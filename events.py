import pygame

# Create Global Events
# Cannot instantiate an event here, unfortinately. Can only generate the int values.
turn_end_e = pygame.USEREVENT + 1
lock_in_e = pygame.USEREVENT + 2  # apply your letters to the board
on_hover_e = pygame.USEREVENT + 3  # if mouse on Tile() class sprite
place_tile_e = pygame.USEREVENT + 4
remove_tile_e = pygame.USEREVENT + 5
game_end_e = pygame.USEREVENT + 6
game_boot_e = pygame.USEREVENT + 7
game_start_e = pygame.USEREVENT + 8
test_button_e = pygame.USEREVENT + 9

# main menu
decrease_players_e = pygame.USEREVENT + 10
increase_players_e = pygame.USEREVENT + 11

on_hover_inv_e = pygame.USEREVENT + 12
test_detect_word_e = pygame.USEREVENT + 13

# placeholder event for the button class
dummy_e = pygame.USEREVENT + 14

server_start_e = pygame.USEREVENT + 15
connect_to_server_e = pygame.USEREVENT + 16
cancel_server_e = pygame.USEREVENT + 17
exchange_tiles_e = pygame.USEREVENT + 18
