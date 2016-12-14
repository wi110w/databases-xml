from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "d3v-lynx"))
session = driver.session()


def create_cities():
    session.run("""match(n:City) detach delete n""")
    session.run("""
                create (m:City {name: "Moscow" }),
                (sb:City {name: "Saint-Petersburg" }),
                (h:City {name: "Helsinki" }),
                (nn:City {name: "Nizhniy Novgorod" }),
                (k:City {name: "Kazan" }),
                (s:City {name: "Saratov" }),
                (sam:City {name: "Samara" }),
                (v:City {name: "Voronez" }),
                (nch:City {name: "Naberezhnye Chelny" }),
                (u:City {name: "Ufa" }),
                (i:City {name: "Izhevsk" }),
                (ch:City {name: "Chelyabinsk" }),
                (p:City {name: "Perm" }),
                (e:City {name: "Ekaterinburg" }),
                (m)-[:road]->(sb), (sb)-[:road]->(h),
                (m)-[:road]->(nn), (nn)-[:road]->(k), (k)-[:road]->(nch),
                (m)-[:road]->(v), (v)-[:road]->(s), (s)-[:road]->(sam),
                (sam)-[:road]->(nch), (nch)-[:road]->(u), (u)-[:road]->(ch),
                (nch)-[:road]->(i), (i)-[:road]->(p), (p)-[:road]->(e),
                (sam)-[:road]->(u),
                (ch)-[:road]->(e)
    """)


def get_nearest_cities(city):
    nearest_cities = session.run(""
                "match (m:City)-[:road*3]->(c:City) where m.name = \"" + city
                                 + "\" return c")
    print("Cities at distance 3 from " + city + ":")
    for city in nearest_cities:
        print(city['c']['name'])


def get_shortest_path(city_from, city_to):
    shortest_path = session.run(""
                "match path=shortestPath((m:City)-[:road*]->(c:City))"
                                "where m.name = \"" + city_from + "\" and c.name =  \"" + city_to
                                + "\" return path")
    print("Shortest path from " + city_from + " to " + city_to + ":")
    for i in shortest_path:
        city = i['path']
        path = ' -> '.join([n['name'] for n in city.nodes])
        print(path)


create_cities()
get_nearest_cities("Samara")
get_shortest_path("Moscow", "Ekaterinburg")