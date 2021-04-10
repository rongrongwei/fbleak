import sqlite3

CONN = sqlite3.connect('public_data/names.db')

def generate_comparison(name_query):
    results = pull_data(name_query)
    if type(results[1][2]) == str or type(results[0][2]) == str:
        ratio = 'unknown'
        percentile = 'unknown'
    else:
        ratio = results[1][2]/results[0][2]
        percentile = pull_percentile(ratio)

    data = {
        'name':name_query,
        'census_count':str(results[0][1]),
        'census_freq':str(results[0][2]),
        'fbleak_count':str(results[1][1]),
        'fbleak_freq':str(results[1][2]),
        'fb_census_ratio':str(ratio),
        'ratio_percentile':str(percentile).replace('0.','')
    }
    return data

def pull_data(name_query):
    name_val = name_query.upper()
    query = """
        SELECT name, count, freq FROM census WHERE NAME = ?
    """
    cursor = CONN.cursor()
    cursor.execute(query, (name_val,))
    census_data = cursor.fetchall()

    query = """
        SELECT name, count, freq FROM fbleak WHERE NAME = ?
    """
    cursor.execute(query, (name_val,))
    fbleak_data = cursor.fetchall()
    cursor.close()

    if len(census_data) == 0:
        census_data = [(name_val, 'unknown', 'unknown')]
    if len(fbleak_data) == 0:
        fbleak_data = [(name_val, 'unknown', 'unknown')]

    return (census_data[0], fbleak_data[0])

def pull_percentile(ratio):
    query = """
    select 
        percentile 
    from 
        percentiles 
    where 
        ratio <= ? 
    order by percentile desc 
    limit 1
    """
    cursor = CONN.cursor()
    cursor.execute(query, (ratio,))
    data = cursor.fetchall()
    if len(data) == 0:
        return 0
    else:
        return data[0][0]

if __name__ == "__main__":
    print(generate_comparison('wei'))