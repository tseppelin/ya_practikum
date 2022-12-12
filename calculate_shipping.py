import decimal


MINIMAL_PRICE = 400


ROUTE_DIST = {
    'under_30': 200,
    'over_30': 300,
    'under_10': 100,
    'under_2': 50
}


DIMENSIONS_COST = {
    'large': 200,
    'small': 100
}


IS_FRAGILE_COST = 300


WORKLOAD_COEF = {
    'extremely high': 1.6,
    'high': 1.4,
    'increased': 1.2,
    'normal': 1
}


class CalculateShippingError(Exception):
    pass


class InputError(CalculateShippingError):
    pass


class ShippingUnavailableError(CalculateShippingError):
    pass


def calculate_shipping_cost(
    distance: float, dimensions: str, is_fragile: bool, service_workload: str
) -> decimal.Decimal:
    """
    Args:
        distance (int): distance from A to B
        dimensions (str): options: 'S' or 'L' - cargo dimensions
        is_fragile (bool): fragily of cargo
        service_workload (str): options: extremely_high, high, increased, normal

    Returns:
        decimal.Decimal: summary cost of shipping
    """
    if service_workload not in WORKLOAD_COEF.keys():
        raise InputError(
            f'Available options for workload: {WORKLOAD_COEF.keys()}')

    if dimensions not in DIMENSIONS_COST.keys():
        raise InputError(
            f'Available options for dimensions: {DIMENSIONS_COST.keys()}')

    if distance <= 0:
        raise InputError('Distance should be > 0')

    trip_cost = 0

    if distance <= 2:
        trip_cost += 50
    if distance > 2 and distance <= 10:
        trip_cost += 100
    if distance > 10 and distance <= 30:
        trip_cost += 200
    if distance > 30 and is_fragile:
        raise ShippingUnavailableError(
            'Fragile goods cannot be transported over a distance of more than 30 km')
    if distance > 30:
        trip_cost += 300

    if dimensions == 'small':
        trip_cost += DIMENSIONS_COST['small']
    elif dimensions == 'large':
        trip_cost += DIMENSIONS_COST['large']

    if is_fragile:
        trip_cost += 300

    workload_coef = WORKLOAD_COEF[service_workload]
    trip_cost = trip_cost * workload_coef
    trip_cost = decimal.Decimal(str(trip_cost))
    trip_cost = round(trip_cost, 2)
    return max(trip_cost, MINIMAL_PRICE)
