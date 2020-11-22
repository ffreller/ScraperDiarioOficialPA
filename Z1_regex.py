import re


def parse_text(texto):
    patt = re.compile('(Protocolo:?  ?\d{6})')
    lt = re.split(patt, texto)
    res = []
    if len(lt[-1]) < 100:
        lt = lt[:-1]
        for con, aa in enumerate(lt):
            if con % 2 != 0:
                res.append(lt[con - 1] + lt[con])
    else:
        for con, aa in enumerate(lt):
            if con % 2 != 0:
                res.append(lt[con - 1] + lt[con])
            if con == len(lt) - 1:
                res.append(lt[con])

    return res


def inconsistencias(txto):
    txt = txto
    txto = txto.replace('\\n', ' ')
    txto = txto.replace('\n', ' ')
    txto = txto.lower()
    patt01 = re.compile('(protocolo:?  ?\d{6})')
    patt02 = re.compile('(bruno yoheiji kono ramos)')
    #ATENÇAO AQUI
    patt0 = re.compile('(presidente ?protocolo \d{6}\d?)')
    patt1 = re.compile(
        '((0?[1-9]|[12][0-9]|3[01])[/ -.](0?[1-9]|1[12])[/ -.](19[0-9]{2}|[2][0-9][0-9]{2}) ?bruno yoheiji kono ramos)')
    patt11 = re.compile('(bruno yoheiji kono ramos [–-] presidente( ?belém ?[(]pa[)],?|governo))')
    patt2 = re.compile('(publique-se)[. ] ?(bruno yoheiji kono ramos)')
    patt3 = re.compile('(gabinete  ?da  ?presidência  ?do  ?instituto  ?de  ?terras  ?do  ?pará ? ?- ?iterpa, ? ?em \d\d? de) (janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) (de 20\d{2}.? protocolo:? \d{6})')

    patt4 = re.compile('(daniel nunes lopes presidente wiliiams e silva fernandes diretor do deaf)')
    patt5 = re.compile('(publique-se)[. ] ?(daniel nunes lopes)')
    patt6 = re.compile('(daniel nunes lopes presidente {4}belém,)')
    res = []
    # print(re.search(patt0, txt))

    if re.search(patt0, txto):
        # print('a1')
        l1 = re.split(patt0, txto)
        for con, a in enumerate(l1):
            if con % 2 != 0:
                res.append(l1[con - 1] + l1[con])
            else:
                if con == len(l1) - 1 and len(l1[con]) > 50:
                    res.append(l1[con])

    elif len(re.findall(patt1, txto)) > 1:
        # print('a2')
        occ = [m.start() for m in re.finditer(patt1, txto)]
        if len(occ) == 2:
            pos = occ[0]
            res.append(txto[:pos + 46])
            res.append(txto[pos + 46:])

        elif len(occ) == 3:
            pos1 = occ[0]
            pos2 = occ[1]
            res.append(txto[:pos1 + 46])
            res.append(txto[pos1 + 46:pos2 + 46])
            res.append(txto[pos2 + 46:])

        else:
            print('problema1')

    elif re.findall(patt11, txto) and len(re.findall(patt02, txto)) > 1:
        # print('a2')
        occ = [m.start() for m in re.finditer(patt11, txto)]

        if len(occ) == 2 or len(occ) == 1:
            pos = occ[0]
            res.append(txto[:pos + 37])
            res.append(txto[pos + 37:])

        elif len(occ) == 3:
            pos1 = occ[0]
            pos2 = occ[1]
            res.append(txto[:pos1 + 37])
            res.append(txto[pos1 + 37:pos2 + 37])
            res.append(txto[pos2 + 37:])

        else:
            print('problema patt11')

    elif len(re.findall(patt2, txto)) > 1:
        # print('a3')
        occ = [[m.start(), m[0]] for m in re.finditer(patt2, txto)]
        if len(occ) == 2:
            pos1 = occ[0][0]
            tamanh = len(occ[0][1])
            res.append(txto[:pos1 + tamanh])
            res.append(txto[pos1 + tamanh:])

        elif len(occ) == 3:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:])

        elif len(occ) == 4:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:])

        elif len(occ) == 5:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:])

        elif len(occ) == 6:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:])

        elif len(occ) == 7:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:])

        elif len(occ) == 8:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            pos7 = occ[6][0]
            tamanh7 = len(occ[6][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:pos7 + tamanh7])
            res.append(txto[pos7 + tamanh7:])

        else:
            print(len(occ))
            print('problema2a')

    elif re.findall(patt3, txto) and len(re.findall(patt01, txto)) > 1:
        # print('a3')
        occ = [[m.start(), m[0]] for m in re.finditer(patt3, txto)]
        if len(occ) == 2 or len(occ) == 1:
            pos = occ[0][0]
            tamanh = len(occ[0][1])
            res.append(txto[:pos + tamanh])
            res.append(txto[pos + tamanh:])

        elif len(occ) == 3:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:])

        elif len(occ) == 4:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:])

        elif len(occ) == 5:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:])

        elif len(occ) == 6:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:])

        elif len(occ) == 7:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:])

        elif len(occ) == 8:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            pos7 = occ[6][0]
            tamanh7 = len(occ[6][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:pos7 + tamanh7])
            res.append(txto[pos7 + tamanh7:])

        else:
            print(len(occ))
            print('problema2b')

    elif len(re.findall(patt5, txto)) > 1:
        # print('a3')
        occ = [[m.start(), m[0]] for m in re.finditer(patt5, txto)]
        if len(occ) == 2:
            pos = occ[0][0]
            tamanh = len(occ[0][1])
            res.append(txto[:pos + tamanh])
            res.append(txto[pos + tamanh:])

        elif len(occ) == 3:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:])

        elif len(occ) == 4:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:])

        elif len(occ) == 5:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:])

        elif len(occ) == 6:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:])

        elif len(occ) == 7:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:])

        elif len(occ) == 8:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            pos7 = occ[6][0]
            tamanh7 = len(occ[6][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:pos7 + tamanh7])
            res.append(txto[pos7 + tamanh7:])

        elif len(occ) == 9:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            pos7 = occ[6][0]
            tamanh7 = len(occ[6][1])
            pos8 = occ[7][0]
            tamanh8 = len(occ[7][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:pos7 + tamanh7])
            res.append(txto[pos7 + tamanh7:pos8 + tamanh8])
            res.append(txto[pos8 + tamanh8:])

        elif len(occ) == 16:
            pos1 = occ[0][0]
            tamanh1 = len(occ[0][1])
            pos2 = occ[1][0]
            tamanh2 = len(occ[1][1])
            pos3 = occ[2][0]
            tamanh3 = len(occ[2][1])
            pos4 = occ[3][0]
            tamanh4 = len(occ[3][1])
            pos5 = occ[4][0]
            tamanh5 = len(occ[4][1])
            pos6 = occ[5][0]
            tamanh6 = len(occ[5][1])
            pos7 = occ[6][0]
            tamanh7 = len(occ[6][1])
            pos8 = occ[7][0]
            tamanh8 = len(occ[7][1])
            pos9 = occ[8][0]
            tamanh9 = len(occ[8][1])
            pos10 = occ[9][0]
            tamanh10 = len(occ[9][1])
            pos11 = occ[10][0]
            tamanh11 = len(occ[10][1])
            pos12 = occ[11][0]
            tamanh12 = len(occ[11][1])
            pos13 = occ[12][0]
            tamanh13 = len(occ[12][1])
            pos14 = occ[13][0]
            tamanh14 = len(occ[13][1])
            pos15 = occ[14][0]
            tamanh15 = len(occ[14][1])
            res.append(txto[:pos1 + tamanh1])
            res.append(txto[pos1 + tamanh1:pos2 + tamanh2])
            res.append(txto[pos2 + tamanh2:pos3 + tamanh3])
            res.append(txto[pos3 + tamanh3:pos4 + tamanh4])
            res.append(txto[pos4 + tamanh4:pos5 + tamanh5])
            res.append(txto[pos5 + tamanh5:pos6 + tamanh6])
            res.append(txto[pos6 + tamanh6:pos7 + tamanh7])
            res.append(txto[pos7 + tamanh7:pos8 + tamanh8])
            res.append(txto[pos8 + tamanh8:pos9 + tamanh9])
            res.append(txto[pos9 + tamanh9:pos10 + tamanh10])
            res.append(txto[pos10 + tamanh10:pos11 + tamanh11])
            res.append(txto[pos11 + tamanh11:pos12 + tamanh12])
            res.append(txto[pos12 + tamanh12:pos13 + tamanh13])
            res.append(txto[pos13 + tamanh13:pos14 + tamanh14])
            res.append(txto[pos14 + tamanh14:pos15 + tamanh15])
            res.append(txto[pos15 + tamanh15:])

        else:
            print(len(occ))
            print('problema2c')

    elif len(re.findall(patt4, txto)) > 1:
        l1 = re.split(patt4, txto)
        for con, a in enumerate(l1):
            if con % 2 != 0:
                res.append(l1[con - 1] + l1[con])
            else:
                if con == len(l1) - 1 and len(l1[con]) > 50:
                    res.append(l1[con])

    elif re.search(patt6, txto):
        if txto.count('governo do estado do pará instituto de terras do pará - iterpa') > 1:
            l1 = re.split(patt6, txto)
            for con, a in enumerate(l1):
                if con % 2 != 0:
                    res.append(l1[con - 1] + l1[con])
                else:
                    if con == len(l1) - 1 and len(l1[con]) > 50:
                        res.append(l1[con])
        else:
            res.append(txto)

    elif txt.count('EDITAL DE NOTIFICAÇÃO') > 1:
        # print('a4')
        f = txt.find('EDITAL DE NOTIFICAÇÃO')+21
        f2 = txt[f:].find('EDITAL DE NOTIFICAÇÃO')
        txt1 = txt[:f2+f]
        txt2 = txt[f+f2:]
        res.append(txt1)
        res.append(txt2)

    else:
        res.append(txto)

    return res


def corrigir_texto(txt):
    patt1 = re.compile('\.\. ?')
    if re.search(patt1, txt):
        txt = re.sub(patt1, '', txt)
    txt = txt.replace('  ', ' ')
    txt = txt.replace('  ', ' ')
    if txt:
        while txt[0] == ' ':
            txt = txt[1:]
    return txt


def get_page(df):
    for row in df.iterrows():
        pgs = []
        txto = row[1][1]
        patt = re.compile(' ? ?(\d?\d{2}\|\|\d) ? ?')
        if len(re.findall(patt, txto)) > 0:
            txt = re.sub(patt, '', txto)
            while txt[0] == ' ':
                txt = txt[1:]
            df.loc[row[0], 'txt'] = txt
            for match in re.findall(patt, txto):
                if match[:match.find('|')] not in pgs:
                    pgs.append(match[:match.find('|')])
            df.loc[row[0], 'page'] = str(pgs)[1:-1]
        else:
            if row[0] == 0:
                df.loc[row[0], 'page'] = '0'
            else:
                df.loc[row[0], 'page'] = df.loc[row[0]-1, 'page']
    return df