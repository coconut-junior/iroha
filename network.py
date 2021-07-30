import subprocess as s
import itertools

def getNetworks():
    p = s.Popen(['/sbin/iw','dev','wlan0','scan'], stdout=s.PIPE)
    r = str(p.communicate()[0]).replace('\n','')
    r = filter(None, [filter(None, item.split('\t')) for item in r.split('Cell')]) # EDITED
    merged = list(itertools.chain.from_iterable(r)) # merge the cells, or just use the index of one cell?
    merged = str(merged)
    merged = merged.split('\\n\\')
    ssids = []

    for line in merged:
        if 'SSID: ' in line:
            ssid = line.replace('\\t','').replace("\\","").replace('SSID: ', '').strip()
            if ssid != '' and not 'x00' in ssid:
                ssids.append(ssid)
    return ssids

print(getNetworks())

