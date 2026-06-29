import geopandas as gpd
from shapely.validation import explain_validity
from shapely.validation import make_valid


def find_duplicates(gdf):    
    duplicates = gdf.duplicated(subset = ['geometry'])     # contains series with boolean answers
    dup_count = duplicates.sum()      # contains count of total duplicate entries for user
    unique_count = (~duplicates).sum() 
    duplicate_rows = gdf[duplicates]

    return duplicate_rows, dup_count, unique_count

def check_validity(gdf):
    # check if geometries are valid
    valid = gdf.geometry.is_valid
    valid_count = (valid).sum()
    invalid_count = (~valid).sum()
    invalid_rows = gdf[(~valid)].copy() 

    invalid_rows['reason'] = invalid_rows.geometry.apply(explain_validity)

    return invalid_rows, valid_count, invalid_count

def fix_invalid(gdf):
    invalid = ~gdf.geometry.is_valid
    gdf.loc[invalid, 'geometry'] = gdf.geometry[invalid].apply(make_valid)
    
    return gdf