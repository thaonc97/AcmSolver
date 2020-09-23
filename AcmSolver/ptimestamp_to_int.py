def protobuf_timestamps_to_dates(protobuf_timestamps):
    """
    Convert protobuf timestamps (string in rfc 3339 format) to interger for easy modelling
    
    Parameters:
    ----------
        protobuf_timestamps:list of protobuf timestamp (rfc 3339 format), e.g. '2020-09-20T00:00:20.000000010Z' (str).
        
    Returns:
    --------
        Time in python datetime.date.
    """
    date_list = []
    
    for protobuf_timestamp in protobuf_timestamps:
        _timestamp = Timestamp()
        _timestamp.FromJsonString(value = protobuf_timestamp)
        _date = _timestamp.ToDatetime().date()
        date_list.append(_date)
        
    return date_list

def get_runing_days(start_date_list,expired_date_list):
    """
    Get total number of campaign running days.
    
    Parameters:
    ----------
        start_date_list: list of start dates (list<datetime>).
        exppired_date_list  list of expired dates (list<datetime>).
        
    Returns:
    --------
        total of running day (int).
    """
    min_d = min(start_date_list)
    max_d = max(expired_date_list)
    num_days = (max_d-min_d).days +1
    return num_days 

def map_datetime_to_int(total_days,start_date):
    """
    map datetime to int.
    
    Parameters:
    ----------
        total_days: total of running day (int).
        start_date:  the youngest date among start dates of problems (datetime).
        
    Returns:
    --------
        a dictionary maps datetimes to intergers (dict<datetime,int>).
    """
    datetime_to_int_map = {}
    
    for _days in range(total_days):
        datetime_to_int_map[start_date + datetime.timedelta(days =_days)] = _days

    return datetime_to_int_map

def map_int_to_p_timestamps(start_timestamps,expired_timestamps):
    """
    map int to protobuf timestamp.
    
    Parameters:
    ----------
        start_timestamps: a list of protobuf timestamp (rfc 3339 format), e.g. '2020-09-20T00:00:20.000000010Z' (str).
        expired_timestamps: a list of protobuf timestamp (rfc 3339 format), e.g. '2020-09-20T00:00:20.000000010Z' (str).
        
    Returns:
    --------
        a dictionary maps model-ready-interger to protobuf timestamp json string (dict<int,string>).
    """
    start_dates_list = protobuf_timestamps_to_dates(start_timestamps)
    expired_dates_list = protobuf_timestamps_to_dates(expired_timestamps)
    youngest_date = min(start_dates_list)
    # oldest_date = max(expired_dates_list)
    total_days = get_runing_days(start_dates_list,expired_dates_list)
    
    int_to_protobuf_timestamps_dict= {}
    
    for int_date in range(total_days):
        cur_date = youngest_date + datetime.timedelta(days =int_date)
        cur_date_time = datetime.datetime(cur_date.year,cur_date.month,cur_date.day)
        cur_timestamp = Timestamp()
        cur_timestamp.FromDatetime(cur_date_time)
        int_to_protobuf_timestamps_dict[int_date] = cur_timestamp.ToJsonString()
        
    return int_to_protobuf_timestamps_dict