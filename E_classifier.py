from pandas import read_csv, DataFrame

# year = 2015
years = [2020, 2019, 2018, 2017, 2016, 2015]


def tirar_hifenespaco(txt, word):
    li = []
    adds = ['-', '.']
    for n in range(0, len(word)):
        if n != 0 and n != (len(word) - 1):
            for add in adds:
                t1 = word[:n]
                t2 = word[n:]
                nword = t1 + add + t2
                li.append(nword)
    for nword in li:
        txt = txt.replace(nword, word)

    li = []
    add = '- '
    for n in range(0, len(word)):
        if n != 0 and n != (len(word) - 1):
            t1 = word[:n]
            t2 = word[n:]
            nword = t1 + add + t2
            li.append(nword)
    for nword in li:
        txt = txt.replace(nword, word)

    li = []
    add = ' '
    for n in range(0, len(word)):
        if n != 0 and n != (len(word) - 1):
            t1 = word[:n]
            t2 = word[n:]
            nword = t1 + add + t2
            li.append(nword)
    for nword in li:
        txt = txt.replace(nword, word)

    return txt


def compra_de_terras(txt):
    txt = txt.lower()
    achar = 'compra de terras'
    nachar = 'diária'
    achou = False
    txt = tirar_hifenespaco(txt, achar)
    if achar in txt and nachar not in txt[:15]:
        achou = True
    return achou


def indeferido(txt):
    txt = txt.lower()
    achar1 = 'regularização fundiária foi indeferido'
    achar2 = 'indeferimento do pedido de regularização fundiária'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if achar1 in txt or achar2 in txt:
        achou = True
    return achou


def cancelamento_titulo(txt):
    txt = txt.lower()
    txt = txt.replace('ﬁ ', 'fi')
    txt = txt.replace('ﬁ', 'fi')
    achar1 = 'cancelar administrativamente'
    achar2 = 'tomar ciência da determinação de cancelamento'
    achar3 = 'falsidade do título definitivo de venda de terras'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    if achar1 in txt or achar2 in txt or achar3 in txt:
        achou = True
    return achou


def resgate_adm(txt):
    txt = txt.lower()
    achar = 'resgate administrativo'
    achou = False
    if tirar_hifenespaco(txt, achar):
        txt = tirar_hifenespaco(txt, achar)
    if achar in txt:
        achou = True
    return achou


def cotacao_eletronica(txt):
    txt = txt.lower()
    achar1 = 'edital de cotação eletrônica'
    achar2 = 'aviso de cotação eletrônica'
    achar5 = 'aviso de cotaç.ão eletrônica'
    achar6 = 'aviso de cotação eletrôn. ica'
    achar3 = 'cotação eletrônica'
    achar4 = 'notificação'
    achar7 = 'instrumento substitutivo de contrato origem'
    achar1 = 'edital cotação eletrônica'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    txt = tirar_hifenespaco(txt, achar4)
    if achar1 in txt or achar2 in txt or achar5 in txt or achar6 in txt or (achar3 in txt and achar4 in txt) \
            or (achar3 in txt and achar7 in txt):
        achou = True
    return achou


def titulo_aforamento(txt):
    txt = txt.lower()
    achar1 = 'títulos de aforamento'
    achar2 = 'renúncia de aforamento'
    achar3 = 'detentor de parte do título de aforamento'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if achar1 in txt or achar2 in txt or achar3 in txt:
        achou = True
    return achou


def servidor_ferias(txt):
    txt = txt.lower()
    achar1 = 'dias de férias'
    achar2 = 'no uso das atribuições que lhe são conferidas no art. 5º, alínea “b” da lei estadual nº 4.584'
    achar3 = 'férias'
    nachar1 = 'tornar sem efeito'
    nachar2 = 'conceder, diárias'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    if achar1 in txt or (achar2 in txt and achar3 in txt):
        if nachar1 not in txt and nachar2 not in txt:
            achou = True
    return achou


def titulo_definitivo(txt):
    txt = txt.lower()
    txt = txt.replace('ﬁ ', 'fi')
    txt = txt.replace('ﬁ', 'fi')
    achar1 = 'reconhecer a existência do título definitivo'
    achar2 = 'ratificação de títulos'
    achar3 = 'beneficiários de títulos definitivos'
    nachar = 'cancelar administrativamente'

    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if achar1 in txt or achar2 in txt or achar3 in txt and nachar not in txt:
        achou = True
    return achou


def apostilamento(txt):
    txt = txt.lower()
    achar = 'apostilamento . apostilamento'
    achou = False
    txt = tirar_hifenespaco(txt, achar)
    if achar in txt:
        achou = True
    return achou


def filiacao_dominial(txt):
    txt = txt.lower()
    achar1 = 'cópia autenticada'
    achar2 = 'dominial'
    achar3 = 'certidão'
    nachar = 'dominial'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    if achar1 in txt and achar2 in txt and achar3 in txt and nachar not in txt:
        achou = True
    return achou

def suspensao_revogacao_licitacao(txt):
    txt = txt.lower()
    achar1 = 'aviso de suspensão de licitação'
    achar2 = 'revogação de licitação'
    achar3 = 'aviso de suspens. ão de licitação'
    achar4 = 'revogação d. e licitação'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar2)
    if achar1 in txt or achar2 in txt or achar3 in txt or achar4 in txt:
        achou = True
    return achou

def ordem_servico(txt):
    txt = txt.lower()
    achar = 'expedir a ordem de serviço'
    achou = False
    txt = tirar_hifenespaco(txt, achar)
    if achar in txt:
        achou = True
    return achou

def prorrogar_prazo(txt):
    txt = txt.lower()
    achar1 = 'prorrogar o prazo, por mais 30 (trinta) dias'
    achar2 = 'prorrogar o prazo, por mais 60 (sessenta) dias'
    achar3 = 'prorrogar, por mais 30 (trinta) dias'
    achar4 = 'prorrogar por 30 (trinta) dias o prazo'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    txt = tirar_hifenespaco(txt, achar4)
    if achar1 in txt or achar2 in txt or achar3 in txt or achar4 in txt:
        achou = True
    return achou

def regularizacao_fundiaria(row):
    txt = row['txt'].lower()
    achar1 = 'regularização fundiária da área'
    achar2 = 'regularização fundiária por reconhecimento de domínio coletivo'
    achar3 = 'regularização fundiária por reconhecimento de dominio coletivo'
    achar4 = 'conclusão da presente regularização fundiária'
    achar5 = 'regularização fundiária das comunidades locais '
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    txt = tirar_hifenespaco(txt, achar4)
    txt = tirar_hifenespaco(txt, achar5)
    if not row['apostilamento'] and not row['indeferido']:
        if achar1 in txt or achar2 in txt or achar3 in txt or achar4 in txt or achar5 in txt:
            achou = True
    return achou


def retificacao(row):
    txt = row['txt'].lower()
    txt = txt.replace('ﬁ', 'fi')
    achar1 = 'termo de retificação'
    achar2 = 'retificação da diferença'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['apostilamento']:
        if achar1 in txt or achar2 in txt:
            achou = True
    return achou


def procedimento_adm(row):
    txt = row['txt'].lower()
    achar = 'procedimento administrativo'
    achou = False
    txt = tirar_hifenespaco(txt, achar)
    if not row['titulo_aforamento'] and not row['prorrogar_prazo']:
        if achar in txt:
            achou = True
    return achou


def servidor_diaria(row):
    txt = row['txt']
    # achar1 = 'DIÁRIAS'
    # achar2 = 'Diárias COLABORADOR'
    # achar3 = 'DIÁRIA'
    # naoachar = 'TORNAR SEM EFEITO'
    achar1 = 'diárias'
    achar2 = 'diárias colaborador'
    achar3 = 'diária'
    naoachar = 'tornar sem efeito'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    if not row['errata'] and not row['processo_seletivo']:
        if (achar1 in txt or achar2 in txt or achar3 in txt[:15]) and naoachar not in txt:
            achou = True
    return achou

def cooperacao_tecnica(row):
    txt = row['txt'].lower()
    achar1 = 'cooperação técnica'
    achar2 = 'termo de cooperação'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['servidor_diaria'] and not row['errata']:
        if achar1 in txt or achar2 in txt:
            achou = True
    return achou


def errata(row):
    txt = row['txt'].lower()
    achar1 = 'errata'
    achar2 = 'onde se lê'
    achar3 = 'leia-se:'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['compra_de_terras'] and not row['retificacao']:
        if achar1 in txt[:25] or (achar1 in txt and achar2 in txt) or achar3 in txt:
            achou = True
    return achou


def processo_seletivo(row):
    achar = 'processo seletivo'
    txt = row['txt'].lower()
    achou = False
    txt = tirar_hifenespaco(txt, achar)
    if not row['errata']:
        if achar in txt:
            achou = True
    return achou


def areas_rurais(row):
    txt = row['txt'].lower()
    achar1 = 'regularização das áreas rurais'
    achar2 = 'regularização da área rural'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['errata'] and not row['nao_onerosa']:
        if achar1 in txt or achar2 in txt:
            achou = True
    return achou


def ccdru(row):
    txt = row['txt'].lower()
    achar1 = 'ccdru'
    achar2 = 'cdru'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['errata'] and not row['servidor'] and not row['servidor_diaria']:
        if achar1 in txt or achar2 in txt:
            achou = True
    return achou


def dispensa_licitacao(row):
    achar = "dispensa de licitação"
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar)
    if not row['errata']:
        if achar in txt[:100]:
            achou = True
    return achou


def resultado_licitacao(row):
    achar = "resultado de licitação"
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar)
    if not row['errata']:
        if achar in txt[:100]:
            achou = True
    return achou


def contrato(row):
    achar1 = 'contratante'
    achar2 = 'cargo/função'
    achar3 = 'contrato'
    achar4 = 'termo aditivo a contrato'
    achar5 = 'extrato de termo aditivo'
    achar6 = 'instrumento substitutivo de contrato nota de empenho'
    achar7 = 'contrato termo aditivo'
    nachar1 = 'terras devolutas'
    nachar2 = 'tornar sem efeito'
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    txt = tirar_hifenespaco(txt, achar4)
    txt = tirar_hifenespaco(txt, achar5)
    txt = tirar_hifenespaco(txt, achar6)
    txt = tirar_hifenespaco(txt, nachar1)
    txt = tirar_hifenespaco(txt, nachar2)
    if not row['dispensa_licitacao'] and not row['errata'] and not row['processo_seletivo']:
        if achar1 in txt or achar4 in txt or achar5 in txt or (achar2 in txt and achar3 in txt)\
                or achar6 in txt or achar7 in txt:
            if nachar1 not in txt and nachar2 not in txt:
                achou = True
    return achou


def servidor(row):
    txt = row['txt'].lower()
    achar1 = 'servidor'
    achar2 = 'cargo comissionado'
    achar3 = 'servido-ra'
    achar4 = 'designar, na forma do art. 5º, letra “j”, da lei nº 4.584/75,'
    achar5 = 'para exercer o cargo'
    nachar = 'protocolo: 206693'
    # origtxt = row['txt']
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    txt = tirar_hifenespaco(txt, achar4)
    if not row['errata'] and not row['contrato'] and not row['procedimento_adm'] and not row['processo_seletivo'] \
            and not row['servidor_diaria'] and not row['servidor_ferias'] and not row['compra_de_terras'] \
            and not row['cotacao_eletronica'] and not row['resultado_licitacao'] and not row['dispensa_licitacao']\
            and not row['retificacao']:
        if achar1 in txt or achar2 in txt or achar3 in txt or achar4 in txt or achar5 in txt:
            if nachar not in txt:
                achou = True
    return achou


def terras_devolutas(row):
    txt = row['txt'].lower()
    achar1 = 'terras devolutas'
    achar2 = 'terras públicas devolutas'
    nachar = 'tornar sem efeito'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, nachar)
    if not row['servidor'] and not row['areas_rurais']:
        if (achar1 in txt or achar2 in txt) and nachar not in txt:
            achou = True
    return achou


def aviso_licitacao(row):
    txt = row['txt'].lower()
    achar1 = 'aviso de licitação'
    achar2 = 'aviso de  reabertu. ra de licitação'
    achar3 = 'aviso de reabertu. ra de licitação'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['servidor'] and not row['errata'] and not row['cotacao_eletronica'] and not row['resultado_licitacao']\
            and not row['suspensao_revogacao_licitacao']:
        if achar1 in txt or achar2 in txt or achar3 in txt:
            achou = True
    return achou


def analise_documentos(row):
    achar = 'análise de documentos'
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar)
    if not row['servidor'] and not row['servidor_ferias'] and not row['cancelamento_titulo']:
        if achar in txt:
            achou = True
    return achou


def notifica_processo_adm(row):
    txt = row['txt'].lower()
    txt = txt.replace('ﬁ ', 'fi')
    txt = txt.replace('ﬁ', 'fi')
    achar1 = 'processo administrativo de seu interesse'
    achar2 = 'processos administrativos de seu interesse'
    achar3 = 'relacionado ao(s) seu(s) processo(s)'
    achar4 = 'processo administrativo em epígrafe'
    achar5 = 'NOTIFICA'
    achar6 = 'edital de notificação'
    achar7 = 'notificam-se os interessados nos processos listados abaixo'
    achou = False
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    txt = tirar_hifenespaco(txt, achar3)
    txt = tirar_hifenespaco(txt, achar4)

    if not row['indeferido']:
        if achar1 in txt or achar2 in txt or achar3 in txt or (achar4 in txt and achar5 in row['txt'])\
                or (achar4 in txt and achar6 in txt) or achar7 in txt:
            achou = True
    return achou


def nao_onerosa(row):
    achar1 = 'não onerosa'
    achar2 = 'doação de terras'
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['procedimento_adm'] and not row['servidor'] and not row['indeferido'] and not row['retificacao'] \
            and not row['notifica_processo_adm'] and not row['ccdru'] and not row['errata'] and not row['servidor_diaria']:
        if achar1 in txt or achar2 in txt:
            achou = True
    return achou


def sem_efeito(row):
    achar1 = 'tornar sem efeito'
    achar2 = 'I – tornar sem efeito'
    nachar = "protocolo 889261"
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['servidor'] and not row['processo_seletivo'] and not row['errata'] and not row['nao_onerosa']:
        if achar1 in txt or achar2 in txt:
            if nachar not in txt:
                achou = True
    return achou


def permuta(row):
    achar = 'permuta'
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar)
    if not row['indeferido'] and not row['notifica_processo_adm'] and not row['errata'] and not row['sem_efeito']\
            and not row['compra_de_terras']:
        if achar in txt:
            achou = True
    return achou


def onerosa(row):
    achar1 = 'onerosa'
    achar2 = '(compra) de terras'
    achou = False
    txt = row['txt'].lower()
    txt = tirar_hifenespaco(txt, achar1)
    txt = tirar_hifenespaco(txt, achar2)
    if not row['notifica_processo_adm'] and not row['servidor'] and not row['nao_onerosa'] and not row['sem_efeito'] \
            and not row['indeferido'] and not row['ccdru'] and not row['retificacao'] and not row['errata'] and not row['servidor_diaria']:
        if achar1 in txt or achar2 in txt:
            achou = True
    return achou

def corrigir20160414(txt):
    ntxt = txt.lower()
    achar = 'pregoeiro protocolo 950405'
    if achar in ntxt:
        tamanh = len(achar)
        loc = ntxt.find(achar)
        txt = txt[:loc+tamanh]
    return txt


def undummy(d):
    return d.dot(d.columns)


def classificar(yr):
    print(yr)
    df = read_csv(f'parsed{yr}.csv', index_col='Unnamed: 0')
    df.rename(columns={'txt': 'txtlinhas'}, inplace=True)
    df['txt'] = df['txtlinhas'].apply(lambda x: x.replace('\n', ' '))

    for row1 in df.iterrows():
        txtlinhas = row1[1][1]
        txtt = row1[1][2]
        if txtt.count('EDITAL DE NOTIFICAÇÃO') > 1:
            achou1 = txtt.find('EDITAL DE NOTIFICAÇÃO') + 21
            achou2 = txtt[achou1:].find('EDITAL DE NOTIFICAÇÃO')
            txt1 = txtt[:achou2 + achou1]
            txt2 = txtt[achou1 + achou2:]

            achou1 = txtlinhas.find('EDITAL DE NOTIFICAÇÃO') + 21
            achou2 = txtlinhas[achou1:].find('EDITAL DE NOTIFICAÇÃO')
            txtlinhas1 = txtlinhas[:achou2 + achou1]
            txtlinhas2 = txtlinhas[achou1 + achou2:]

            print('Usou o mecanismo')

            df.drop(row1[0], inplace=True)
            df2 = DataFrame({'filename': [row1[1][0], row1[1][0]],
                             'txtlinhas': [txtlinhas1, txtlinhas2],
                             'txt': [txt1, txt2]})
            df = df.append(df2, ignore_index=True)

    df['txt'] = df['txt'].apply(corrigir20160414)
    df['compra_de_terras'] = df['txt'].apply(compra_de_terras)
    df['indeferido'] = df['txt'].apply(indeferido)
    df['cancelamento_titulo'] = df['txt'].apply(cancelamento_titulo)
    df['ordem_servico'] = df['txt'].apply(ordem_servico)
    df['resgate_adm'] = df['txt'].apply(resgate_adm)
    df['titulo_aforamento'] = df['txt'].apply(titulo_aforamento)
    df['cotacao_eletronica'] = df['txt'].apply(cotacao_eletronica)
    df['servidor_ferias'] = df['txt'].apply(servidor_ferias)
    df['titulo_definitivo'] = df['txt'].apply(titulo_definitivo)
    df['apostilamento'] = df['txt'].apply(apostilamento)
    df['filiacao_dominial'] = df['txt'].apply(filiacao_dominial)
    df['suspensao_revogacao_licitacao'] = df['txt'].apply(suspensao_revogacao_licitacao)
    df['prorrogar_prazo'] = df['txt'].apply(prorrogar_prazo)
    df['retificacao'] = df.apply(retificacao, axis=1)
    df['procedimento_adm'] = df.apply(procedimento_adm, axis=1)
    df['errata'] = df.apply(errata, axis=1)
    df['processo_seletivo'] = df.apply(processo_seletivo, axis=1)
    df['servidor_diaria'] = df.apply(servidor_diaria, axis=1)
    df['cooperacao_tecnica'] = df.apply(cooperacao_tecnica, axis=1)
    df['dispensa_licitacao'] = df.apply(dispensa_licitacao, axis=1)
    df['resultado_licitacao'] = df.apply(resultado_licitacao, axis=1)
    df['regularizacao_fundiaria'] = df.apply(regularizacao_fundiaria, axis=1)
    df['contrato'] = df.apply(contrato, axis=1)
    df['servidor'] = df.apply(servidor, axis=1)
    df['ccdru'] = df.apply(ccdru, axis=1)
    df['aviso_licitacao'] = df.apply(aviso_licitacao, axis=1)
    df['analise_documentos'] = df.apply(analise_documentos, axis=1)
    df['notifica_processo_adm'] = df.apply(notifica_processo_adm, axis=1)
    df['nao_onerosa'] = df.apply(nao_onerosa, axis=1)
    df['sem_efeito'] = df.apply(sem_efeito, axis=1)
    df['permuta'] = df.apply(permuta, axis=1)
    df['onerosa'] = df.apply(onerosa, axis=1)
    df['areas_rurais'] = df.apply(areas_rurais, axis=1)
    df['terras_devolutas'] = df.apply(terras_devolutas, axis=1)

    #PROCURAR ERROS (DUPLICATAS)
    contador = 0
    for r in df.iterrows():
        nn = 0
        for nu in range(3, len(df.columns)):
            nn += r[1][nu]
        if nn > 1:
            contador += 1
            print('***********')
            print(r)
            print(r[1][2])
    print('Duplicados:', contador)
    #CRIAR OUROS
    df['outros'] = False
    for row1 in df.iterrows():
        t = row1[1][3:].sum()
        if t != 1:
            df.loc[row1[0], 'outros'] = True

    # CHECAR RESULTADOS
    for a in df.columns[3:]:
        print(a, df[a].sum())

    df1 = df.assign(classificacao=df.filter(df.columns[3:]).pipe(undummy))
    df1.drop(columns='txt', inplace=True)
    df1.rename(columns={'txtlinhas': 'txt'}, inplace=True)
    df1.to_csv(f'categorizado{yr}.csv')


for year in years:
    classificar(year)
    print('\n')
# classificar(year)
