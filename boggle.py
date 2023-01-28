#################################################################
# FILE : boggle.py
# WRITERS : nicole gurevich
# EXERCISE : intro2cs2 ex12 2022
# DESCRIPTION : Boggle game
#################################################################
from tkinter import *
from tkinter import messagebox
from ex12_utils import read_wordlist, get_board, is_near


class Screen:

    def __init__(self):
        """vars"""
        self.board = get_board()  # random matrix of letters
        self.length_board = len(get_board())  # length of the rows\coloumns of
        # the matrix
        self.word = ""  # current word being formed by the player
        self.clock_time = 180  # set amount of time to run the game (in secs)
        self.dictionary = read_wordlist('boggle_dict.txt')  # dictionary for
        # the game
        self.found_word_bank = []  # list of all the words found
        self.score = 0  # player's score
        self.path_current = []  # current path the user is taking

        """start screen"""
        self.root = Tk()
        self.root.config(bg='#F565AE')
        self.title = self.root.title("boggle game screen")  # screen title
        self.size = self.root.geometry("700x600")  # screen default size
        self.frame = Frame(self.root, bg='#DC92F5', width=200, height=550)
        self.frame.place(relx=.5, rely=.4, anchor="center")
        self.welcome = Label(self.frame, bg='#DC92F5',
                             text="welcome to boggle\nlets play!",
                             font=("forte", 30))  # create welcome sign
        self.welcome.pack()
        self.start_button = Button(self.frame, bg='#7CC9F2',
                                   text='press to start the game',
                                   font=("forte", 13), command=self.start_game)
        # create start button
        self.start_button.pack()
        self.info = Button(self.frame, bg='#7CC9F2',
                           text='press for instructions', font=("forte", 13),
                           command=self.instructions)  # create start button
        self.info.pack()
        self.root.mainloop()

    def instructions(self):
        """instructions page"""
        self.welcome.destroy()
        self.start_button.destroy()
        self.info.destroy()
        self.title_info = Label(self.root, bg='#DC92F5',
                                text='BOGGLE INSTRUCTIONS', font=("forte", 20))
        self.title_info.pack(side=TOP)
        self.explanation = \
            Label(self.frame, bg='#DC92F5', text= '*boggle is played with 16 '
                                                  'random letters,\nyou will '
                                                  'play with randomly generated'
                                                  ' letters\n*you have 3 '
                                                  'minutes (shown by countdown'
                                                  ' timer)\n to find as many '
                                                  'words as you can in the grid'
                                                  ',\n according to the '
                                                  'foloowing rules:\n- the'
                                                  ' letters must be adjoining'
                                                  ' in a "chain"\n(buttons in '
                                                  'the chain may be adjacent '
                                                  'horizontally, vertically or '
                                                  'diagonally)\n- you can only '
                                                  'guess each word once\n- when'
                                                  ' the time runs out the game'
                                                  ' will end and your score '
                                                  'will be shown,\nyou will be '
                                                  'given the option to restart'
                  , font=("forte", 14), width= 65, height= 19)
        self.explanation.pack()
        self.info = Button(self.root, bg='#7CC9F2',
                           text='press to start game', font=("forte", 13),
                           command=self.start_game_from_instructions)
        # create start button
        self.info.pack(side=BOTTOM)

    def start_game_from_instructions(self):
        """command for start_button to start the game from the
        instructions page"""
        self.title_info.destroy()
        self.frame.destroy()
        self.info.destroy()
        self.main_screen()

    def start_game(self):
        """command for start_button to start the game"""
        self.welcome.destroy()
        self.start_button.destroy()
        self.info.destroy()
        self.main_screen()  # call the function that runs the main game

    def main_screen(self):
        """frames the entire screen"""
        self.title = Label(self.root, bg='#DC92F5',
                                text='BOGGLE',
                                font=("forte", 20))
        self.title.pack(side=TOP)
        self.main_frame = LabelFrame(self.root, text="Lets Play Boggle")
        self.main_frame.pack(fill="both", expand=True)



        """LEFT SIDE"""
        # create left frame
        self.left_frame = Frame(self.main_frame, width=500, height=570)
        self.left_frame.pack(side=LEFT)
        # current word section
        self.current_word_section()
        # letter matrix section
        self.matrix_section()

        """RIGHT SIDE"""
        # create rifht frame
        self.right_frame = Frame(self.main_frame,width=200, height=550)
        self.right_frame.pack(side=RIGHT)
        # found words section
        self.found_words_section()
        # score section
        self.score_section()
        # time section
        self.time_section()


    """LEFT SIDE: matrix and current word functions"""
    def matrix_section(self):
        """display letters grid"""
        self.left_botoom_frame = LabelFrame(self.left_frame, bg='#7CC9F2',
                                            width=300, height=500,
                                            text='MATRIX')  # create frame
        self.left_botoom_frame.pack(side=BOTTOM)
        self.buttons_for_matrix_section()  # call function that
        # creates the buttons

    def buttons_for_matrix_section(self):
        """func that creates the buttons for the game"""
        for i in range(self.length_board):
            for j in range(self.length_board):
                Button(self.left_botoom_frame, text=str(self.board[i][j]),
                       width=9,height=3, bg='#F565AE', fg='white',
                       font=("forte", 16), command= lambda i=i, j=j:
                    self.add_letter(self.board[i][j], i, j))\
                    .grid(row=i, column=j)  # create each button with command
                # to add to current word

    def add_letter(self, button, i, j):
        """add letter clicked to current word"""
        self.word += button  # update the current word being displayed on the
        # screen according to the button clicked
        self.path_current.append((i, j))  # create the current path taken in
        # order to check validity
        self.cur_word_Label.config(text=self.word)  # update the label in the
        # current word section

    def current_word_section(self):
        """display the word that is currently formed"""
        self.left_top_frame = LabelFrame(self.left_frame, bg='#7CC9F2'
                                         , width=400, height=100,
                                         text='current word')  # create frame
        self.left_top_frame.pack(side=TOP)
        self.cur_word_Label = Label(self.left_top_frame,
                                    bg='#7CC9F2', fg="white", text='',
                                    font=('forte', 15), width=30, height=6)
        # create label to display the current word
        self.cur_word_Label.pack(side=LEFT)
        self.submission = Button(self.left_top_frame,
                                 text= "sumbit word\nfor checking", width=10,
                                 bg='#DC92F5', font=('arial', 8),
                                 command=self.is_word_found)  # create button
        # to check if the word is correct
        self.submission.pack(side=RIGHT)
        self.delete = Button(self.left_top_frame, text="delete letter",
                             width=10, height=2, font=('arial', 8),
                             bg='#F565AE', command=self.delete_letter)
        # create a button that deletes the last  letter
        self.delete.pack(side=RIGHT)

    def delete_letter(self):
        """delete last letter in current word"""
        self.word = self.word[0:-1]
        self.cur_word_Label.config(text=self.word)
        self.path_current.pop()


    """RIGHT: time,score, and found words functions"""
    def found_words_section(self):
        """display found words"""
        self.right_top_frame = LabelFrame(self.right_frame, bg='#7CC9F2',
                                          width=180, height=300,
                                          text='found words')
        self.right_top_frame.pack(side=TOP)
        self.label_found = Label(self.right_top_frame,
                                 text="", bg='#DC92F5', fg="white",
                                 font=("forte", 12), height=19, width=20)
        self.label_found.pack(side=TOP)

    def is_word_found(self):
        """ checks if the word is in the dictionary/ is found from a correct
        path/ hasn't been found yet.
        if so add it to the found words list and update score if not tell
        the player he made a mistake"""
        if self.is_valid_path():  # if path is a valid path
            if not self.compare_words():  # if the word hasn't been found before
                if self.word in self.dictionary:
                    self.found_word_bank.append(str(self.word))
                    self.label_found.config(text="\n".join(self.found_word_bank))
                    self.score += len(self.path_current) ** 2  # update score
                    self.score_label.config(text=str(self.score))  # if word is
                    # in dictionary add to the score
                elif self.word not in self.dictionary:  # message to the player
                    self.label_found.config(text="wrong guess try again")
            else:  # message to the player
                self.label_found.config(text="you already\n found that "
                                             "word\nlook for a new one")
        else:
            self.label_found.config(text="incorrect path, try again")  # if
            # path is invalid
        self.word = ""  # if the players guessed correct or wrong always
        # reset the current word
        self.cur_word_Label.config(text=self.word)
        self.path_current = []

    def compare_words(self):
        """check if the current word is not in found_word_bank"""
        for word in self.found_word_bank:
            if word == self.word:
                return True
        return False

    def is_valid_path(self):
        """check if move is valid"""
        used_path = []
        for i in range(len(self.path_current) - 1):
            used_path.append(self.path_current[i])
            if self.path_current[i + 1] not in is_near(self.path_current[i][0],
                                                       self.path_current[i][1])\
                    or self.path_current[i + 1] in used_path:
                return False
        return True

    def time_section(self):
        """display the clock"""
        self.right_bottom_frame = LabelFrame(self.right_frame,
                                             bg='#7CC9F2', height=150,
                                             width=180, text='time')  #create
        # frame for the time
        self.right_bottom_frame.pack(side=BOTTOM)
        self.clock_min = Label(self.right_bottom_frame, width=6, text="03",
                               font=('forte', 20))  # create minutes label
        self.clock_min.pack(side=LEFT)
        self.clock_sec = Label(self.right_bottom_frame, width=6, text="00",
                               font=('forte', 20))  # create seconds label
        self.clock_sec.pack(side=RIGHT)
        self.timer()  # start the countdown timer

    def timer(self):
        """countdown recursive timer function"""
        min, sec = self.clock_time // 60, self.clock_time % 60  # get value in
        # min\sec
        self.clock_min.config(text="0" + str(min))  # update min label
        self.clock_sec.config(text=str(sec))  # update sec label
        if self.clock_time > -1:  # condition: while the time is still running
            self.root.after(1000, self.timer)  # delay the function
            # one second each call
            self.clock_time -= 1
        else:
            if messagebox.askretrycancel('retry',
                                         'time is up\nyour score is: '
                                         + str(self.score) + '\ndo you want '
                                                             'to try again?'):
                # when the time runs out ask the player if he wants to quit
                # or play again
                self.root.destroy()
                play_again = Screen()
            else:
                self.root.destroy()

    def score_section(self):
        """display score"""
        self.right_middle_frame = LabelFrame(self.right_frame,
                                             bg='#7CC9F2', height=150,
                                             width=180, text='score')  # create
        # frame
        self.right_middle_frame.pack()
        self.score_label = Label(self.right_middle_frame, bg='#DC92F5',
                                 fg="white", width=12, height=2, text="0",
                                 font=('forte', 20))  # create score label
        self.score_label.pack(side=TOP)


screen = Screen()

