# findTopology, findCorner 的传参修改为笔画列
import findTopology, findCorner
from os.path import join, dirname
from sqlite3 import connect
from contextlib import closing
from re import compile as RE
import sys

def write(con, attr, data, job='new', dtype=None):
    if job=='new':
        con.execute('CREATE TABLE {0} (name VARCHAR(8), {0} {1});'.format(attr, dtype))
    elif job=='renew':
        con.execute('DELETE FROM {}'.format(attr))
    else:
        raise ValueError
    con.execute("INSERT INTO {} VALUES {};".format(str(data).strip('[]')))
    con.commit()

def readStorkes(con):
	strokePattern = RE(r'(?<=\d)(?=M)')
	for name, feature, svg in con.execute(
	    '''
	    SELECT name, feature, svg
	    FROM main
	    WHERE level = 0
	    '''
	):
	    features = feature.split(',')
	    svgs = strokePattern.split(svg)
	    strokes = [Stroke(feature, svg) for feature, svg in zip(features, svgs)]
	    yield name, strokes

def cacheLevel(con, job='new'):
	cur = con.execute('SELECT name, first, second FROM main;')
    res = {i[0]:{} if i[1] is None else {'f':i[1], 's':i[2]} for i in cur}
    def setLevel(n, l=0):
        obj = res[n]
        if obj.get('f') is None:
            obj.setdefault('l', 0)
        else:
            l = obj.setdefault('l', max(setLevel(obj['f'], l), setLevel(obj['s'], l)))
        return l + 1
    for name in res:
        setLevel(name)
    levels = [(name, res[name]['l']) for name in res]
    write(con, 'level', levels, job=job, dtype='INTEGER')

def cacheTopo(con, job='new'):
	topos = []
    for name, strokes in readStorkes(con):
	    topo = ''.join([str(i) for j in findTopology(strokes) for i in j])
	    topos.append((name, topo))
	write(con, 'topo', topos, job=job, dtype='VARCHAR(200)')

def cacheCorner(con, job='new'):
    corners = []
	for name, strokes in readStorkes(con):
	    corner = str(list(findCorner(strokes))).strip('()').replace(' ', '')
	    corners.append((name, corner))
	write(con, 'corner', corners, job=job, dtype='VARCHAR(50)')


# example
if __name__ == '__main__':
	dbInFile = sys.argv[1]
	dbPath = join(dirname(__file__), dbInFile)
	job = sys.argv[2]
	part = sys.argv[3:]
	with closing(connect(dbPath)) as con:
		if 'level' in part: cacheLevel(con, job=job)
		if 'topo' in part: cacheTopo(con, job=job)
		if 'corner' in part: cacheCorner(con, job=job)
