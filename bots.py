import threading
import time
import json

# open the file and load it into a json object
with open('inventory.dat', 'r') as inventory_file:
    inventory = eval(inventory_file.read())


def bot_clerk(items):
    cart = []
    lock = threading.Lock()
    fetcher_lists = [[] for _ in range(3)]

    # Separate items into robot fetcher lists
    for i, item in enumerate(items):
        fetcher_lists[i % 3].append(item)

    # Launch each robot fetcher using a new thread
    threads = []
    for i, fetcher_list in enumerate(fetcher_lists):
        thread = threading.Thread(target=bot_fetcher, args=(fetcher_list, cart, lock))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return cart

def bot_fetcher(items, cart, lock):
    for item in items:
        item_number = item
        # Get the item description from the inventory dictionary
        item_description = inventory.get(item_number, ["Unknown Item"])[0]

        # Simulate fetching item from the warehouse
        time.sleep(inventory.get(item, [0])[1])

        # Ensure proper locks to avoid race conditions while appending to cart
        with lock:
            cart.append([item_number, item_description])