import easygui as eg
import os
from Fase_1.sprint2_fase1_script import sprint2_fase1
from Fase_2.sprint2_fase2_script import sprint2_fase2
from Util.downloader_e_contador_locs_repositorios import runScriptDownloaderContadorLocsRepositoriosMain
from Util.exportador_lista_loc_csv import runExportadorListaLocCsvScriptMain
from Util.verificador_repositorios import runVerificadorErrosLocRepositoriosScriptMain

def mainScript():
    titulo = "Laboratório de Experimentação de Software - Sprint 2"
    pergunta = "Qual fase da Sprint 2 você deseja executar?"
    listaDeOpcoes = ["Fase 1", "Fase 2"]
    #listaDeOpcoes = ["Fase 1", "Fase 2", "Fase 3", "Fase 4"]
    escolha = eg.choicebox(pergunta, titulo, listaDeOpcoes)
    cls()

    if(escolha is None):
        print("A operação foi cancelada e nenhuma fase foi escolhida.")
    else:
        fase_escolhida = switchFaseDaSprint(escolha)
        
        delegarChamadaFase(fase_escolhida)
        runScriptDownloaderContadorLocsRepositoriosMain(fase_escolhida)
        runExportadorListaLocCsvScriptMain(fase_escolhida)
        runVerificadorErrosLocRepositoriosScriptMain(fase_escolhida)


def switchFaseDaSprint(fase_escolhida_checkbox):
    return {
        'Fase 1': r'\Fase_1',
        'Fase 2': r'\Fase_2',
        'Fase 3': r'\Fase_3',
        'Fase 4': r'\Fase_4'
    }.get(fase_escolhida_checkbox, "Fase nao escolhida")


def delegarChamadaFase(fase):
    if(fase == r'\Fase_1'):
        sprint2_fase1()
    elif(fase == r'\Fase_2'):
        sprint2_fase2()
    elif(fase == r'\Fase_3'):
        print("To be implemented")
        #sprint2_fase3()
    elif(fase == r'\Fase_4'):
        print("To be implemented")
        #sprint2_fase4()
    else:
        print("A escolha não foi efetuada, nenhuma sprint foi iniciada")
        return

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

mainScript()
