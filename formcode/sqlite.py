import sqlite3

def select_all():
    with sqlite3.connect('db/tracks.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT TrackName,Difficulty,Conditions,Date from Medalists")
        medalists = cursor.fetchall()
        return medalists

def select_track(track):
    trackname=track
    with sqlite3.connect("db/tracks.db") as db:
        cursor = db.cursor()
        cursor.execute("SELECT TrackName,Difficulty,Conditions,Date from Medalists WHERE TrackName='{0}'".format(trackname))
        medalists = cursor.fetchall()
        return medalists
    
def add_track():
    track_name = input("Please enter the track name: ")
    difficulty = input("Please enter the difficulty: ")
    conditions = input("Please enter the conditions: ")
    date = input("Please enter the date: ")

    newrecord = (track_name.capitalize(), difficulty, conditions.capitalize(), date)

    with sqlite3.connect("db/tracks.db") as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Medalists(TrackName,Difficulty,Conditions,Date) VALUES (?,?,?,?)",newrecord)
        db.commit()


def main():
    print("\nWhat would you like to see? ")
    print("1. All tracks")
    print("2. Show certain track")
    choice = input("Please enter your choice (1, 2 or 3) ")
    if choice == "1":
        tracks = select_all()
        for row in tracks:
            print("{0} {1} {2} {3}".format(row[0], row[1], row[2], row[3]))
    elif choice == "2":
        track = input("Which track do you want? ")
        tracks = select_track(track)
        for row in tracks:
            print("{0} {1} {2} {3}".format(row[0], row[1], row[2], row[3]))
    elif choice =="3":
        add_track()    
    main()

main()
