# Stdlib imports

def extract(sel, xpath, sep=' '):
    return clean(compact(textify(sel.xpath(xpath).extract(), sep)))


def extract_data(data, path, delem=''):
    return delem.join(i.strip() for i in data.xpath(path).extract() if i).strip()


def extract_distinct(data, path, delem='\n'):
    return delem.join(i.strip() for i in data.xpath(path).extract() if i).strip()


def extract_list_data(data, path):
    return data.xpath(path).extract()


def get_nodes(data, path):
    return data.xpath(path)