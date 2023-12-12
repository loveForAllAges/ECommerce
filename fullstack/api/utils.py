
def get_obj(prefix, table, item, query_list):
    try:
        return query_list.append((prefix, item, table.objects.get(pk=item).name))
    except:
        return query_list
