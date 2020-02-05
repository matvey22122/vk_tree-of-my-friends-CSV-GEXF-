import vk_api
import networkx


LOGIN = "" #<- логин от ВК
PASSWORD = "" #<- пароль от ВК

FILENAME_CSV = "users.csv"
FILENAME_GEPHI = "users.gexf"

def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)

    vk_session.auth()
    vk = vk_session.get_api()

    list_of_friends = vk.friends.get()

    users_friends = {}
    users_friends[vk.users.get()[0]['id']] = vk.friends.get()['items']

    for i in list_of_friends['items']:
        try:
            users_friends[i] = vk.friends.get(user_id=i)['items']
        except:
            continue
    
    
    graph = networkx.Graph()

    already_added = set()

    for user_key in list(users_friends):
        user_id = str(user_key)

        graph.add_node(user_id, label=user_id)
        already_added.add(user_id)

        for friend_id in users_friends[user_key]:

            if str(friend_id) in already_added:
                continue

            graph.add_node(str(friend_id), label=str(friend_id))
            graph.add_edge(user_id, str(friend_id))

    networkx.write_adjlist(graph, FILENAME_CSV)

    networkx.write_gexf(graph, FILENAME_GEPHI)

if __name__ == "__main__":
    main()