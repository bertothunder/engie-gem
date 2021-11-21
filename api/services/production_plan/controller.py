import typing
import logging
import operator
import pandas as pd


logger = logging.getLogger('api.services.production_plan.controller')


def get_cost_per_fuel_type(data: typing.Dict, fuel_type: str) -> float:
    # Default return value will be for wind, at 0 cost.
    cost = 0.0
    if fuel_type == 'gasfired':
        cost = float(data['fuels']['gas(euro/MWh)'])
    elif fuel_type == 'turbojet':
        cost = float(data['fuels']['kerosine(euro/MWh)'])
    return cost


def get_types(plants: typing.List[typing.Dict]) -> typing.List[str]:
    all_types = [plant['type'] for plant in plants]
    # Return the unique values
    return list(set(all_types))


def process(data):
    # Obtain the initial dataframe from the data, only from 'powerplants' section
    df = pd.json_normalize(data, record_path=['powerplants'])
    logger.debug(f'Read data: {df}')

    required_load = float(data['load'])
    logger.info(f'Required load: {required_load}')

    # Parse the data to obtain the fuel types and the costs per type
    fuel_types = get_types(data['powerplants'])
    fuel_costs = {fuel_type: get_cost_per_fuel_type(data, fuel_type) for fuel_type in fuel_types}
    logger.debug(f'Fuel costs: {fuel_costs}')

    # Now sort the types by the cost in ascending order
    fuel_costs = dict(sorted(fuel_costs.items(), key=operator.itemgetter(1)))

    # Now get the reduction factors: for wind it will read the value in the payload,
    # otherwise it will assign a factor or 1.
    factors = []
    for key, _ in fuel_costs.items():
        if key == 'windturbine':
            factors.append(float(data['fuels']['wind(%)'] / 100))
        else:
            factors.append(1.0)

    # Create a new dataframe with  weigths, production costs, sorting keys and efficiency factors for each
    # plant type, so we obtain a mapped powerplant -> fuel set.
    df_map = pd.DataFrame({'type': fuel_costs.keys(),
                           'cost': fuel_costs.values(),
                           'factor': factors})

    # Reorder the dataframe now by type.
    #
    # type          index    cost     factor
    # windturbine    0       0.0         0.6
    # gasfired       1      13.4         1.0
    # turbojet       2      50.8         1.0
    sorted_map = df_map.reset_index().set_index('type')
    logger.debug(f'First sorted mapped data: {sorted_map}')

    # Now generate a working dataframe incorporating all the fields from the weighted dataframe above
    df['type_idx'] = df['type'].map(sorted_map['index'])
    df['cost'] = df['type'].map(sorted_map['cost'])
    df['factor'] = df['type'].map(sorted_map['factor'])

    #  Let's obtain now the data sorted by efficiency, power and all other necessary factors.
    #  - type (ascending)
    #  - plant efficiency (descending)
    #  - minimal power (descending)
    #  - max power (descending)
    # We will also remove intermediate columns. So we obtain a dataset with the right entering order in the
    # electrical grid
    df2 = df.sort_values(by=['type_idx', 'efficiency', 'pmin', 'pmax'], ascending=[True, False, False,
                                                                                   False]).reset_index()
    df_sorted = df2.drop(labels=['type_idx'], axis=1)

    # At this point, this is what we should have in the sorted dataframe
    #    name                       type        efficiency  pmin   pmax    cost    factor
    # 0  windpark1                  windturbine       1.00     0   150      0.0       0.6
    # 1  windpark2                  windturbine       1.00     0    36      0.0       0.6
    # 2  gasfiredbig1               gasfired          0.53   100   460     13.4       1.0
    # 3  gasfiredbig2               gasfired          0.53   100   460     13.4       1.0
    # 4  gasfiredsomewhatsmaller    gasfired          0.37    40   210     13.4       1.0
    # 5  tj1                        turbojet          0.30     0    16     50.8       1.0

    # Now we need to calculate intermediate data, like hourly-generated energy given plant's min and max power,
    # reduction factor (wind %, only for wind plants). No ramping factor considered here, so we forget about min
    # values, only max values.
    #
    # - Maximum energy to be produced by the plant
    df_sorted['pmax_generated'] = df_sorted.pmax.mul(df_sorted.efficiency).mul(df_sorted.factor)

    # Calculate production figures, including rolling sum of the generated production
    # First row will start with the desired production value, and we will rest the value  for each next row.
    df_sorted.loc[0, 'remaining'] = required_load - df_sorted.loc[0, 'pmax_generated']
    for i in range(1, len(df_sorted)):
        df_sorted.loc[i, 'remaining'] = df_sorted.loc[i - 1, 'remaining'] - df_sorted.loc[i, 'pmax_generated']

    # Now get the production for each plant to to get the desired load
    if df_sorted.loc[0, 'remaining'] >= df_sorted.loc[0, 'pmax_generated']:
        df_sorted.loc[0, 'usage'] = df_sorted.loc[0, 'pmax_generated']
    else:
        df_sorted.loc[0, 'usage'] = 0

    for i in range(1, len(df_sorted)):
        if df_sorted.loc[i - 1, 'remaining'] >= df_sorted.loc[i, 'pmax_generated']:
            df_sorted.loc[i, 'usage'] = df_sorted.loc[i, 'pmax_generated']
        else:
            if df_sorted.loc[i - 1, 'remaining'] >= 0:
                df_sorted.loc[i, 'usage'] = df_sorted.loc[i-1, 'remaining']
            else:
                df_sorted.loc[i, 'usage'] = 0

    # Now we have all data ready, let's clean up the unnecessary columns to return the data
    df_sorted.drop(labels=['index', 'remaining', 'pmax_generated'], axis=1, inplace=True)
    logger.debug(f'Sorted results after calculations: {df_sorted}')

    # At this time this is the expected result figure:
    #
    #   name                        type        efficiency   pmin   pmax   cost factor  remaining  usage
    # 0 windpark1                   windturbine       1.00      0    150    0.0    0.6      390.0   90.0
    # 1 windpark2                   windturbine       1.00      0     36    0.0    0.6      368.4   21.6
    # 2 gasfiredbig1                gasfired          0.53    100    460   13.4    1.0      124.6  243.8
    # 3 gasfiredbig2                gasfired          0.53    100    460   13.4    1.0     -119.2  124.6
    # 4 gasfiredsomewhatsmaller     gasfired          0.37     40    210   13.4    1.0     -196.9    0.0
    # 5 tj1                         turbojet          0.30      0     16   50.8    1.0     -201.7    0.0

    # Now return the final dict with only the name and the usage for each plant
    result = []
    for idx, row in df_sorted[['name', 'usage']].iterrows():
        result.append({
            'name': row['name'],
            'p': round(row['usage']),
        })
    return result
