[app]

# Το όνομα της εφαρμογής
title = FlagQuizApp

# Το πακέτο της εφαρμογής (αυτό θα είναι το π.χ. com.example.flagquiz)
package.name = flagquiz
package.domain = org.example

# Έκδοση της εφαρμογής
version = 0.1

# Κύριο αρχείο Python της εφαρμογής (αυτό που περιέχει την κλάση FlagQuizApp)
source.dir = .

# Εισαγωγή απαραίτητων καταλόγων και αρχείων για την εφαρμογή
source.include_exts = py,png,jpg,kv,atlas,json

# Αποκλεισμός αρχείων και καταλόγων που δεν χρειάζονται να περιληφθούν
source.exclude_dirs = tests,__pycache__

# Γενικές ρυθμίσεις για το Android
osx.python_version = 3
requirements = kivy, pillow

# Ρυθμίσεις για την συσκευή
android.permissions = INTERNET
android.minapi = 21
android.sdk = 28
android.ndk = 21.1.6352462

# Γραφική διεπαφή (UI)
fullscreen = 0
orientation = portrait

# Ρυθμίσεις για τον εκτελέσιμο κώδικα
warn_on_root = 1
