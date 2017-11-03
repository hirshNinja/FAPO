

class MidiConfig():
  def __init__(self):
    self.inputLaunchpadTest = False
    self.lampToggle = True
    self.outputMidi = "IAC Driver IAC Bus 1"  # input MIDI Port, lamps - channel 1, solenoids - channel 2, command - channel 3
    self.inputMidi = "IAC Driver IAC Bus 2" # on - channel 1, off - channel 2, command - channel 3
    self.midiStartGame = 0      # Output & Input MIDI Note (C0) for Starting Game
    self.midiBallStarting = 3   # Output & Input MIDI Note (C#0) for Ball Starting
    self.midiNextMode = 2   # Output & Input MIDI Note for Next Mode
    self.disableMaxCtrl = True
    self.midiLaunchpadMap = {

       0  :'L11',     # LAMP MATRIX ###
       1  :'L21',
       2  :'L31',
       3  :'L41', 
       4  :'L51',
       5  :'L61', 
       6  :'L71',
       7  :'L81',

      16  :'L12',
      17  :'L22',
      18  :'L32',
      19  :'L42',
      20  :'L52',
      21  :'L62',
      22  :'L72',
      23  :'L82',

      32  :'L13',
      33  :'L23',
      34  :'L33',
      35  :'L43',
      36  :'L53',
      37  :'L63',
      38  :'L73',
      39  :'L83',

      48  :'L14',
      49  :'L24',
      50  :'L34',
      51  :'L44',
      52  :'L54',
      53  :'L64',
      54  :'L74',
      55  :'L84',

      64  :'L15',
      65  :'L25',
      66  :'L35',
      67  :'L45',
      68  :'L55',
      69  :'L65',
      70  :'L75',
      71  :'L85',

      80  :'L16',
      81  :'L26',
      82  :'L36',
      83  :'L46',
      84  :'L56',
      85  :'L66',
      86  :'L76',
      87  :'L86',

      96  :'L17',
      97  :'L27',
      98  :'L37',
      99  :'L47',
      100 :'L57',
      101 :'L67',
      102 :'L77',
      103 :'L87',

      112 :'L18',
      113 :'L28',
      114 :'L38',
      115 :'L48',
      116 :'L58',
      117 :'L68',
      118 :'L78',
      119 :'L88',

    ### FLASHER COILS ###

      104 : 'C17',
      105 : 'C18',
      106 : 'C19',
      107 : 'C20',
      108 : 'C23',
      109 : 'C24',

    ### General Illumination ###

      110 : 'G03',
      111 : 'G05'
      # G01, G02, G04 (backglass lights)
    }

