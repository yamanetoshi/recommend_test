# -*- coding:utf-8 -*-

def create_vector(list):
    if (list == []):
        return
    h = {}
    for page in list:
        if (h.has_key(page)):
            h[page] += 1
        else:
            h[page] = 1
    all = {}
    size = float(len(list))
    for page, count in h.items():
        all[page] = count / size
    return all

def similarity(base, target):
    if (base == {} or target == {}):
        return 0.0
    return matrix(base, target) / (abs(base) * abs(target))

def matrix(base, target):
    ret = 0.0
    for key, val in base.items():
        if (target.get(key, "null") == "null"):
            continue
        ret += float(val) * float(target[key])
    return ret

def abs(vec):
    ret = 0.0
    for v in vec.values():
        ret += float(v) * float(v)
    return ret

def recommend(list, page_hash, user_hash):
    vec = create_vector(list)
    if (vec == []):
        return []
    pages = {}
    for page, ratio in vec.items():
        users = page_hash[page].keys()
        if (len(users) == 0):
            continue
        for u in users:
            user_vec = user_hash[u]
            if (len(user_vec) == 0):
                continue
            sim = similarity(vec, user_vec)
            pages[page] = {}
            for _h, _r in user_vec.items():
                if (pages[page].has_key(_h)):
                    pages[page][_h] += float(_r) * sim * float(ratio)
                else:
                    pages[page][_h] = float(_r) * sim * float(ratio)
    ret = {}
    for page, h in pages.items():
        tmp = []
        for p, val in h.items():
            if (p == page):
#            if (vec.has_key(page)):
                continue
            tmp.append([p, round(val, 4)])
        tmp.sort(cmp = lambda x , y: cmp(y[1],x[1]))
        ret[page] = tmp
    return ret

data = [{"user": 1, "page": 0}, {"user": 1, "page": 1}, {"user": 1, "page": 2}, 
        {"user": 1, "page": 3}, {"user": 1, "page": 4}, {"user": 1, "page": 5}, 
        {"user": 1, "page": 6}, {"user": 1, "page": 7}, {"user": 1, "page": 8}, 
        {"user": 1, "page": 9}, 
        {"user": 2, "page": 1}, {"user": 2, "page": 2}, {"user": 2, "page": 3}, 
        {"user": 2, "page": 4}, {"user": 2, "page": 1}, {"user": 2, "page": 2}, 
        {"user": 2, "page": 3}, {"user": 2, "page": 1}, {"user": 2, "page": 2}, 
        {"user": 2, "page": 1}, 
        {"user": 3, "page": 9}, {"user": 3, "page": 9}, {"user": 3, "page": 9}, 
        {"user": 3, "page": 9}, {"user": 3, "page": 9}, {"user": 3, "page": 8}, 
        {"user": 3, "page": 8}, {"user": 3, "page": 8}, {"user": 3, "page": 8}, 
        {"user": 3, "page": 8}, 
        {"user": 4, "page": 8}, {"user": 4, "page": 8}, {"user": 4, "page": 7}, 
        {"user": 4, "page": 5}, {"user": 4, "page": 7}, {"user": 4, "page": 6}, 
        {"user": 4, "page": 6}, {"user": 4, "page": 5}, {"user": 4, "page": 4}, 
        {"user": 4, "page": 4}, 
        {"user": 5, "page": 3}, {"user": 5, "page": 3}, {"user": 5, "page": 3}, 
        {"user": 5, "page": 3}, {"user": 5, "page": 2}, {"user": 5, "page": 4}, 
        {"user": 5, "page": 4}, {"user": 5, "page": 4}, {"user": 5, "page": 4}, 
        {"user": 5, "page": 5}]

print "data is " 
print data 

user_access_count = {}
for item in data:
    if (user_access_count.has_key(item["user"])):
#        print item["user"]
#        print item["page"]
        inner_dict = user_access_count[item["user"]]
        if (inner_dict.has_key(item["page"])):
            inner_dict[item["page"]] += 1
        else:
            inner_dict[item["page"]] = 1
    else:
        inner_dict = {}
        inner_dict[item["page"]] = 1
        user_access_count[item["user"]] = inner_dict

#print user_access_count

user_access_total = {}
for item in data:
    if (user_access_total.has_key(item["user"])):
        user_access_total[item["user"]] += 1
    else:
        user_access_total[item["user"]] = 1

#print user_access_total

user_pmf = {}
for u, h in user_access_count.items():
#    print u
#    print h
    for p, c in h.items():
#        print p
#        print c
#        print user_access_total[u]
        if (user_pmf.has_key(u)):
            user_pmf[u][p] = c/float(user_access_total[u])
        else:
            tmp = {}
            tmp[p] = c/float(user_access_total[u])
            user_pmf[u] = tmp
#        print user_pmf[u]

page_pmf = {}
for u, h in user_pmf.items():
    for p, v in h.items():
        if (page_pmf.has_key(p)):
            page_pmf[p][u] = v
        else:
            tmp = {}
            tmp[u] = v
            page_pmf[p] = tmp

x = recommend(page_pmf.keys(), page_pmf, user_pmf)
print "recommend returns " 
print x 

