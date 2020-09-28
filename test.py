from a2_support import *

"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from a2_support import *

# Fill these in with your details
__author__ = "{{user.name}} ({{user.id}})"
__email__ = ""
__date__ = "2020.9.25"

# Write your code here
class GameLogic:
    def __init__(self, dungeon_name="game1.txt"):
        """Constructor of the GameLogic class.
        Parameters:
            dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        #you need to implement the Player class first.
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._wall = Wall()
        self._key = Key()
        self._door = Door()
        self._moveIncrease = MoveIncrease()
        self.Entity_dic = {
            PLAYER: self._player,
            KEY: self._key,
            DOOR: self._door,
            WALL: self._wall,
            MOVE_INCREASE: self._moveIncrease
        }
        #you need to implement the init_game_information() method for this.
        self._game_information = self.init_game_information()
        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))

        return positions

    def get_dungeon_size(self):
        '''
        Returns the width of the dungeon as an integer.
        '''
        return len(self._dungeon[0])
        
    def init_game_information(self):
        '''
        This method should return a dictionary containing the position and the corresponding 
        Entity as the keys and values respectively. This method also sets the Player’s 
        position. At the start of the game this method should be called to find the position 
        of all entities within the current dungeon.
        '''
        position_dic = {}
        for i in range(len(self._dungeon)):
            for j in range(len(self._dungeon[0])):
                if self._dungeon[i][j] == PLAYER:
                    self._player.currentPosition = (i, j)
                if self._dungeon[i][j] != ' ':
                    entity = self.Entity_dic[self._dungeon[i][j]]
                    position_dic[(i, j)] = entity 
        return position_dic
    
    def get_game_information(self):
        '''
        Returns a dictionary containing the position and the corresponding Entity, 
        as the keys and values, for the current dungeon.
        '''
        position_dic = {}
        for i in range(len(self._dungeon)):
            for j in range(len(self._dungeon[0])):
                if self._dungeon[i][j] != ' ':
                    entity = self.Entity_dic[self._dungeon[i][j]]
                    position_dic[(i, j)] = entity
        return position_dic
        
    def get_player(self):
        '''
        This method returns the Player object within the game.
        '''
        return self._player
        
    def get_entity(self, position):
        '''
        Returns an Entity at a given position in the dungeon. 
        Entity in the given direction or if the position is off map then this function 
        should return None.
        '''
        if position[0] > self.get_dungeon_size() - 1 or position[1] > self.get_dungeon_size() - 1 or position[0] < 0 or position[1] < 0:
            return 
        return self.get_game_information()[position]
        
    def get_entity_in_direction(self, direction: str):
        '''
        Returns an Entity in the given direction of the Player’s position. 
        If there is no Entity in the given direction or if the direction is off map 
        then this function should return None.
        '''
        newPos = (self._player.currentPosition[0] + DIRECTIONS[direction][0], self._player.currentPosition[1] + DIRECTIONS[direction][1])
        if newPos[0] > self.get_dungeon_size() - 1 or newPos[1] > self.get_dungeon_size() - 1 or newPos[0] < 0 or newPos[1] < 0:
            return 
        return self.get_game_information()[newPos]
        
    def collision_check(self, direction: str):
        '''
         Returns ​False​ if a player can travel in the given direction, they won’t collide. 
         ​True, they will collide, otherwise
        '''
        newEntity = self.get_entity_in_direction(direction)
        if newEntity == self._wall:
            return True
        return False
        
    def new_position(self, direction: str):
        '''
        Returns a tuple of integers that represents the new position given the direction.
        '''
        newPos = (self._player.currentPosition[0] + DIRECTIONS[direction][0], self._player.currentPosition[1] + DIRECTIONS[direction][1])
        if (newPos[0] < self.get_dungeon_size() and newPos[0] > -1) and (newPos[1] < self.get_dungeon_size() and newPos[1] > -1 ):
            return newPos
        return self._player.currentPosition
 
    def move_player(self, direction: str):
        '''
        Update the Player’s position to place them one position in the given direction.
        '''
        self._player.currentMoveCount += 1 # update the move count
        if not self.collision_check(direction):
            self._player.currentPosition = self.new_position(direction) # update current position
            self._player.add_item(self.get_entity_in_direction(direction)) # update the inventory
             
    def check_game_over(self):
        '''
        Return True if the game has been ​lost and False otherwise. 
        '''
        if self._player.moves_remaining() < 0:
            return True
        return False

        
    def set_win(self, win):
        '''
        Set the game’s win state to be True or False.
        '''
        self._win = win
        
    def won(self):
        '''
        Return game’s win state(bool).
        '''
        player_inventory = self._player.get_inventory()
        if self._player.moves_remaining() > -1 and (KEY in player_inventory) and self._player.currentPosition in self.get_positions(DOOR): 
            self.set_win(True)
        else:
            self.set_win(False)
        return self._win

class Entity:
    '''
    door, item, player, wall
    '''
    def __init__(self, entity='Entity'):
        self.entity = entity
        self.canCollied = True
        self.entityId = 'Entity'
    
    def get_id(self):
        '''
        Returns a string that represents the Entity’s ID.
        '''
        return self.entityId
    
    def set_collide(self, collidable: bool):
        '''
        Set the collision state for the Entity to be True.
        '''
        self.canCollied = collidable
        
    def can_collide(self):
        '''
        Returns True if the Entity can be collided with (another Entity can share the position 
        that this one is in) and False otherwise.
        '''
        return self.canCollied
    
    def __str__(self):
        '''
        Returns the string representation of the Entity.
        '''
        retStr = self.entity + '(' + '\'' + self.entityId + '\'' + ')'
        return retStr
    def __repr__(self):
        '''
        Same as str(self).
        '''
        retStr = self.entity + '(' + self.entityId + ')'
        return retStr

class Door(Entity):
    def __init__(self):
        self.entity = 'Door'
        self.canCollied = True
        self.entityId = DOOR
    
    def on_hit(self, game: GameLogic):
        '''
        If the Player’s inventory contains a Key Entity then this method should set the 
        ‘game over’ state to be True.
        '''
    
class Item(Entity):
    def __init__(self):
        self.entity = 'Item'
        self.canCollied = True
        self.entityId = 'Entity'
    def on_hit(self, game: GameLogic):
        '''
        This function should raise the NotImplementedError.
        '''
        raise NotImplementedError("NotImplementedError")
    
class Player(Entity):
    def __init__(self, move_count):
        self.entity = 'Player'
        self.canCollied = True
        self.entityId = PLAYER
        self.currentPosition = None
        self.currentMoveCount = 0
        self.inventory = []
        self.move_count = move_count
        
    def set_position(self, position):
        '''
        Sets the position of the Player.
        '''
        self.currentPosition = position
    def get_position(self):
        '''
        Returns a tuple of ints representing the position of the Player. 
        If the Player’s position hasn’t been set yet then this method should return None.
        '''
        return self.currentPosition
    
    def change_move_count(self, number: int):
        '''
        number to be added to the Player’s move count.
        '''
        self.currentMoveCount += number
        
    def moves_remaining(self):
        '''
        Returns an int representing how many moves the Player has left before they reach the maximum move count.
        '''
        return self.move_count - self.currentMoveCount
    def add_item(self, item):
        '''
        Adds the item to the Player’s Inventory. 
        '''
        self.inventory.append(item)
    def get_inventory (self): 
        '''
        Returns a list that represents the Player’s
        inventory. If the Player has nothing in their inventory then an empty list should be returned.
        '''
        return self.inventory      
    
class Wall(Entity):
    def __init__(self):
        self.entity = 'Wall'
        self.canCollied = False
        self.entityId = WALL
        

class MoveIncrease(Item):
    def __init__(self):
        self.entity = 'MoveIncrease'
        self.canCollied = True
        self.entityId = MOVE_INCREASE
        
    def on_hit(self, game: GameLogic):
        '''
        When the player hits the MoveIncrease (M) item the number of moves for the player 
        increases and the M item is removed from the game. These actions are implemented via 
        the on_hit method. Specifically, extra moves should be granted to the Player and the 
        M item should be removed from the game.
        '''
        # TODO:
        
    
class Key(Item):
    def __init__(self):
        self.entity = 'Key'
        self.canCollied = True
        self.entityId = KEY
    
    def on_hit(self, game: GameLogic):
        '''
        When the player takes the Key the Key should be added to the Player’s inventory. 
        The Key should then be removed from the dungeon once it’s in the Player’s inventory.
        '''
        # TODO:

class GameApp:
    def __init__(self):
        self.game = GameLogic()
        self.display = Display(self.game.init_game_information(), self.game.get_dungeon_size())

    def play(self):
        '''
        Handles the player interaction.
        '''

    def draw(self):
        '''
        Displays the dungeon with all Entities in their positions. 
        ​This method should also display the player’s remaining move count
        '''
        print(self.display._game_information)
        self.game.init_game_information()
        self.display.display_game(self.game._player.currentPosition)
        self.display.display_moves(self.game._player.moves_remaining())


game = GameLogic()
print(game.init_game_information())

