import streamlit as st
from file_handler import read_geojson
import folium
from streamlit_folium import st_folium
from shapely.ops import transform
from geometry_utils import find_duplicates, check_validity, fix_invalid
from logger import setup_logger
logger = setup_logger()
from ai_assistant import ask_assistant

# Ttile of the webpage
st.title('GeoJSON Dashboard')
st.markdown("Upload and explore GeoJSON farm polygon data.")
st.divider()

# initialize sessions 
if 'gdf' not in st.session_state:
    st.session_state.gdf = None

if 'duplicates_removed' not in st.session_state:
    st.session_state.duplicates_removed = False

if 'invalid_fixed' not in st.session_state:
    st.session_state.invalid_fixed = False

# option to upload file by user
uploaded_file = st.file_uploader(label="Upload your json or geojson file", type=['geojson', 'json'], )

# warnings and errors during uploading
if uploaded_file is not None:
    # load only once and never reload from file again
    if st.session_state.gdf is None:
        st.session_state.gdf = read_geojson(file=uploaded_file)
    
    # always work from session state
    gdf = st.session_state.gdf
    st.success('File uploaded successfully')
    logger.info(f"File uploaded: {uploaded_file.name}")
    
    # show table in a expander and remove the tabel if updated so only updated table is shown to user
    if not st.session_state.duplicates_removed and not st.session_state.invalid_fixed:
        with st.expander("View and edit the table(Geometry cannot be edited)"):
            edited_df = st.data_editor(
                gdf,
                num_rows="dynamic",
                key="main_table",
                column_config={
                    "geometry": st.column_config.TextColumn(disabled=True)
                }
            )
            # update only non-geometry columns
            for col in edited_df.columns:
                if col != 'geometry':
                    st.session_state.gdf[col] = edited_df[col]

    # display the map using folium
    # first find the centre of total extend of bounds 
    bounds = gdf.total_bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2

    map_display = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    # map_display.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

  
    # to display the shapefiles in map
    folium.GeoJson(gdf).add_to(map_display)

    # to view the polygon and map on web
    if not st.session_state.duplicates_removed and not st.session_state.invalid_fixed:
        with st.expander("View Polygons on Map"):
            st_folium(map_display, width=900, height= 500)
    
    # code to find duplicate entries with warning 
    duplicate_rows, dup_count, unique_count = find_duplicates(gdf)
    logger.warning(f"{dup_count} duplicates found")  # logger warning for duplicates

    # general info about the duplicate parts
    if not st.session_state.duplicates_removed:
        st.warning(f"{dup_count} duplicate geometries found")
        with st.expander("Duplicate geomtery info"):
            st.info(f"Total duplicates: {dup_count} | Unique geometries: {unique_count}")
            st.dataframe(duplicate_rows)

    else:
        st.success("No duplicate geometries found")

    # button to removee the duplicate entries for user
    if not st.session_state.duplicates_removed:
        if st.button("Remove Duplicates"):
            st.session_state.gdf = gdf.drop_duplicates(subset=['geometry'])
            st.session_state.duplicates_removed = True
            st.success("Duplicates removed successfully")
            st.dataframe(gdf)
            logger.info("Duplicates removed by user")


    # code to find invalid entries with warning 
    invalid_rows, valid_count, invalid_count = check_validity(gdf)
    if invalid_count > 0:
        logger.warning(f"{invalid_count} invalid geometries found")


    # general info about the invalid parts
    if not st.session_state.invalid_fixed:
        st.warning(f"{invalid_count} invalid geometries found")
        with st.expander("Invalid geometries info"):
            st.info(f"Total invalid: {invalid_count} | Valid geometries: {valid_count}")
            st.dataframe(invalid_rows)

    else:
        st.success("No invalid geometries found")

    # button to remove the invalid entriesfor user
    if not st.session_state.invalid_fixed:
        if st.button("Fix Invalid Geometries"):
            st.session_state.gdf = fix_invalid(gdf)
            st.session_state.invalid_fixed = True
            st.success("Invalid geometries fixed")
            st.dataframe(gdf)
            logger.info("Invalid geometries fixed by user")


    # final updated editabel df with fixes
    if st.session_state.duplicates_removed or st.session_state.invalid_fixed:
        st.subheader("Updated Data")
        st.data_editor(
            gdf,
            num_rows="dynamic",
            key="updated_table",
            column_config={
                "geometry": st.column_config.TextColumn(disabled=True)
            }
        )

        # show updated map
        updated_map = folium.Map(location=[center_lat, center_lon])
        updated_map.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
        folium.GeoJson(gdf).add_to(updated_map)
        with st.expander("View Updated Polygons on Map"):
            st_folium(updated_map, width=900, height=500, key="updated_map")
    

    st.download_button(
        label="Download Final GeoJSON",
        data=gdf.to_json(),
        file_name="updated_farms.geojson",
        mime="application/json"
    )

    ## Summary for the ai assistnat to get introduced to thtis particular context
    data_summary = f"""
    - Total geometries: {len(gdf)}
    - Duplicate geometries: {dup_count}
    - Invalid geometries: {invalid_count}
    - Columns: {list(gdf.columns)}
    - CRS: {gdf.crs}
    - Geometry types: {gdf.geometry.geom_type.unique().tolist()}
    """
    st.divider()
    st.subheader("Ask about your data")
    question = st.chat_input("e.g. How many geometries? Total duplicates?")
    if question:
        answer = ask_assistant(question, data_summary)
        st.chat_message("user").write(question)
        st.chat_message("assistant").write(answer)
    
else:
    st.warning('No file suploaded')




