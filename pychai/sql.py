from sqlite3 import connect
from yaml import BaseLoader, load
main = connect('pychai/data/main')
cursor = main.cursor()
# cursor.execute('ALTER TABLE main ADD COLUMN svg VARCHAR(1000)')
# cursor.execute('ALTER TABLE main ADD COLUMN feature VARCHAR(200)')
COMPONENTS = load(open('/Users/tansongchen/Library/Git/chai/pychai/data/components.yaml'), BaseLoader)
for name, strokeList in COMPONENTS.items():
    svgStringList = []
    featureList = []
    for stroke in strokeList:
        feature = stroke['feature']
        startString = 'M' + ' '.join(stroke['start'])
        curveString = ''.join([curve['command'] + ' '.join(curve['parameterList']) for curve in stroke['curveList']])
        svgString = startString + curveString
        featureList.append(feature)
        svgStringList.append(svgString)
    cursor.execute('UPDATE main SET svg = ?, feature = ? WHERE name = ?;', (''.join(svgStringList), ','.join(featureList), name))
main.commit()
main.close()
