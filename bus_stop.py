import folium
import streamlit as st
import joblib
import pandas as pd
from folium.plugins import Fullscreen, minimap, Search, MarkerCluster, AntPath

from streamlit_folium import st_folium, folium_static


@st.cache_data
def load_data():
    gwanak_boundary = joblib.load("gwanak_boundary")
    stop_cnt = pd.read_csv("./src/bus_stop_cnt.csv")
    return gwanak_boundary, stop_cnt


def create_map(boundary, stop_cnt):
    # folium map객체 생성
    m = folium.Map(location=[37.478428, 126.931862])
    
    # 관악구 경계 생성 후 이를 위한 feature group 생성
    b_points = [(i[1], i[0]) for i in boundary]
    boundary_group = folium.FeatureGroup(name='관악구 경계')
    boundary_group.add_to(m)
    folium.PolyLine(b_points, weight=2, opacity=1, color='purple', name='관악구 경계선').add_to(boundary_group)
    
    # 모든 정류소 마커 생성
    bus_stop_fg = MarkerCluster(name="버스 정류장", show=False)
    bus_stop_fg.add_to(m)
    for _, stop in stop_cnt.iterrows():
        folium.Marker(location = [stop['y'], stop['x']],
            tooltip=stop['name'],
            name=stop['name'],
            icon=folium.Icon(color='orange',prefix='fa',icon='bus')
            ).add_to(bus_stop_fg)

    # 정류소 검색창 생성
    Search(layer=bus_stop_fg,search_zoom=20 ,search_label='name', placeholder="정류소 위치 검색").add_to(m)

    m.fit_bounds([[37.4421012, 126.831755], [37.5467284, 127.0857543]])
    return m

# 데이터 로드 및 캐싱
gwanak_boundary, stop_cnt = load_data()

m=create_map(gwanak_boundary, stop_cnt)

Fullscreen().add_to(m)
minimap.MiniMap(zoom_level_offset=-5,toggle_display=True).add_to(m)
folium.TileLayer("Stamen Watercolor").add_to(m)
folium.TileLayer("CartoDB dark_matter").add_to(m)
# call to render Folium map in Streamlit
folium.LayerControl().add_to(m)
st_folium(m,height=700,width=700,returned_objects=[])


