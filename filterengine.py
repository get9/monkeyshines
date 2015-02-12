def filter_links(urlos, url_list, blacklist):
    # Keep adding stuff here to filter it out.
    links = urlos
    links = filter(lambda x: x not in blacklist, links)
    links = filter(lambda x: x not in url_list, links)
    return links
