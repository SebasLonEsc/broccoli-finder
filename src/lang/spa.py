from src.logic.constants.infoMenuContent import CREDITS_MENU_MESSAGE_SPA, ABOUT_MENU_MESSAGE_SPA

spanish = {
  # CONSOLE TEXT
  "InputTotalRows": "Número de filas:",
  "InputTotalColumns": "Número de columnas:",
  "InputTotalBroccolis": "Número de brocolis:",
  "GameTypeSelectTitle": "Tipo de juego:",
  "ConsoleTypeSelect": "1: En consola",
  "UITypeSelect": "2: Interfaz gráfica",
  "GameTypeInput": "Ingrese # del tipo de juego:",
  "InvalidGameType": "Número inválido",
  "InputRow": "",
  "InputColumn": "",
  "InvalidRowColumn": "Columna o fila inválida",

  # UI
  "GameTitle": "Broccoli Finder",
  "Exit": "Salir",
  "Winning_Texts": ["Felicitaciones\nGanaste el juego!!",
                    "Lo lograste!!!",
                    "Eso fue increible!",
                    "Pero que habilidos@!!"],
  "Losing_Texts": ["Lo siento perdiste",
                   "Intentalo nuevamente :(",
                   "Yo se que para la próxima\nlo lograrás!!",
                   "Hiciste lo que pudiste"],

  # MENU
  "GameTabMenu": "Juego",
  "MainMenuLabel": "Menú Principal",
  "InfoTabMenu": "Info",
  "AboutMenuLabel": "Acerca",
  "AboutMessage": ABOUT_MENU_MESSAGE_SPA,
  "CreditsMenuLabel": "Créditos",
  "CreditsMessage": CREDITS_MENU_MESSAGE_SPA,
  "NewGameLabel": "Nuevo Juego",

  # NEW GAME VIEW
  "NewGame": "Nuevo Juego",
  "Difficulty": "Dificultad",
  "GameDifficulties": [
    "Facil",
    "Normal",
    "Dificil"
  ],
  "Facil": "Easy", # To translate to Eng to process on code
  "Normal": "Normal", # To translate to Eng to process on code
  "Dificil": "Hard", # To translate to Eng to process on code
  "Small": "Pequeño",
  "Medium": "Mediano",
  "Big": "Grande",
  "CustomGameButton": "Personalizar",

  # CUSTOM GAME VIEW
  "InputErrorText": "Los siguientes campos no son válidos:",
  "InvalidRowLowerLimit": "# Filas no puede ser menor a ",
  "InvalidRowUpperLimit": "# Filas no puede ser mayor a ",
  "InvalidColumnLowerLimit": "# Columnas no puede ser menor a ",
  "InvalidColumnUpperLimit": "# Columnas no puede ser mayor a ",
  "ZeroBroccolisError": "# Brocolis no puede ser menor a 1",
  "BroccoliErrorLimit1": "# Brocolis no puede ser mayor a ",
  "BroccoliErrorLimit2": "para el tamaño actual del tablero",
  "InvalidNumericValue": "Valor no númerico",
  "TooManyBroccolisError": "Reduzca la cantidad de brocolis a no mayor de ",
  "CustomGameTitle": "Personaliza tu juego",
  "InputRowNumber": "# Filas",
  "InputColumnNumber": "# Columnas",
  "InputBroccoliNumber": "# Brocolis",
  "PlayButton": "Jugar",
}