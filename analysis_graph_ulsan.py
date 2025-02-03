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

# 울산광역시의 도로 네트워크를 불러옵니다
place_name = "Ulsan, South Korea"
G = ox.graph_from_place(place_name, network_type="drive")
fig, ax = ox.plot_graph(G, node_color='y')

# # 기본 통계 계산
# stats = ox.stats.basic_stats(G)
#
# # 통계 결과 출력
# print("Basic Stats:")
# for key, value in stats.items():
#     print(f"{key}: {value}")
#
# # DataFrame으로 통계 결과 저장
# stats_df = pd.DataFrame(list(stats.items()), columns=["Stat", "Value"])
#
# # DataFrame 출력
# print("\nStatistical DataFrame:")
# print(stats_df)
#
# # 통계 결과를 CSV 파일로 저장 (선택사항)
# stats_df.to_csv("basic_stats_ulsan.csv", index=False)
#
# # convert graph to line graph so edges become nodes and vice versa
# edge_centrality = nx.closeness_centrality(nx.line_graph(G))
# nx.set_edge_attributes(G, edge_centrality, 'edge_centrality')
#
#
# # color edges in original graph with closeness centralities from line graph
# ec = ox.plot.get_edge_colors_by_attr(G, 'edge_centrality', cmap='inferno')
# fig, ax = ox.plot_graph(G, edge_color=ec, edge_linewidth=2, node_size=0)

#start point, end point
orig = list(G)[0]
dest = list(G)[120]

route = ox.shortest_path(G, orig, dest, weight = 'length')
fig1_1, ax = ox.plot_graph_route(G, route, node_color='y', route_linewidth=6, node_size=0.5)

routes = ox.k_shortest_paths(G, orig, dest, k=30, weight='length')
fig1_2, ax = ox.plot_graph_routes(G, list(routes), node_color='y', route_linewidths=4, node_size=0.5)

G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

edges = ox.graph_to_gdfs(G, nodes=False)
edges['highway'] = edges['highway'].astype(str)
mean_num = edges.groupby('highway')[['length', 'speed_kph', 'travel_time']].mean().round(1)

orig = list(G)[1]
dest = list(G)[120]
route1 = ox.shortest_path(G, orig, dest, weight = 'length')
route2 = ox.shortest_path(G, orig, dest, weight = 'travel_time')

fig2, ax = ox.plot_graph_routes(G, routes=[route1, route2], route_colors=['r', 'y'], route_linewidths=6, node_size=0)