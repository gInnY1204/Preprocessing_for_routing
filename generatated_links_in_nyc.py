import osmnx as ox
import logging
import pandas as pd
import networkx as nx
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors

# 캐시 비활성화
ox.settings.use_cache = True

# 디버그 로그 수준을 "WARNING"으로 설정하여 불필요한 디버그 메시지 숨기기
logging.getLogger('matplotlib').setLevel(logging.WARNING)

# get road data
place_name = "New York City, New York, USA"
G = ox.graph_from_place(place_name, network_type="drive")
fig, ax = ox.plot_graph(G, node_color='r')

# 기본 통계 계산
stats = ox.stats.basic_stats(G)

# 통계 결과 출력
print("Basic Stats:")
for key, value in stats.items():
    print(f"{key}: {value}")

# DataFrame으로 통계 결과 저장
stats_df = pd.DataFrame(list(stats.items()), columns=["Stat", "Value"])

# DataFrame 출력
print("\nStatistical DataFrame:")
print(stats_df)

# 통계 결과를 CSV 파일로 저장 (선택사항)
stats_df.to_csv("basic_stats_"+place_name+".csv", index=False)

# convert graph to line graph so edges become nodes and vice versa
edge_centrality = nx.closeness_centrality(nx.line_graph(G))
nx.set_edge_attributes(G, edge_centrality, 'edge_centrality')


# color edges in original graph with closeness centralities from line graph
ec = ox.plot.get_edge_colors_by_attr(G, 'edge_centrality', cmap='inferno')
fig, ax = ox.plot_graph(G, edge_color=ec, edge_linewidth=2, node_size=0)


# # 2️⃣ 엣지(도로 링크) 데이터프레임으로 변환
# edges = ox.graph_to_gdfs(G, nodes=False)
#
# # 3️⃣ links.csv 형태로 저장할 데이터 가공
# links_df = pd.DataFrame({
#     "link_id": edges.index.map(lambda x: x[2]),  # 링크 ID (OSM의 edge ID)
#     "begin_node_id": edges.index.map(lambda x: x[0]),  # 시작 노드 ID
#     "end_node_id": edges.index.map(lambda x: x[1]),  # 끝 노드 ID
#     "startX": edges['u'].map(lambda x: G.nodes[x]['x']),  # 시작점 경도
#     "startY": edges['u'].map(lambda x: G.nodes[x]['y']),  # 시작점 위도
#     "endX": edges['v'].map(lambda x: G.nodes[x]['x']),  # 끝점 경도
#     "endY": edges['v'].map(lambda x: G.nodes[x]['y']),  # 끝점 위도
#     "street_length": edges['length'],  # 도로 길이 (m)
#     "travel_time": 0,  # 기본값 (추후 계산)
#     "speed_limit": 0,  # 기본값 (추후 속도 제한 추가)
#     "elevation": 0,  # 기본값 (고도 정보 추가 가능)
#     "carbon_emission": 0  # 기본값 (추후 CO2 배출량 계산 가능)
# })
#
# # 4️⃣ CSV 파일로 저장
# links_df.to_csv("./data/links.csv", index=False)
#
# print("✅ links.csv 파일이 생성되었습니다!")
