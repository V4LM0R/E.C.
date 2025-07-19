from flask import Flask, render_template, request, redirect, url_for, flash, session
import random
import json

app = Flask(__name__)
app.secret_key = 'candy-exchange-secret-key-2025'

# Almacenamiento en memoria (sin base de datos)
games_storage = {}
current_game_id = None

class Game:
    def __init__(self):
        self.id = random.randint(1000, 9999)
        self.phase = 1
        self.status = 'setup'  # setup, phase1, phase2, finished
        self.players = {}
        self.exchanges = []
        
    def add_player(self, name):
        if len(self.players) >= 20:
            return False
        if name in self.players:
            return False
        
        self.players[name] = {
            'name': name,
            'limon_count': 0,
            'pera_count': 0,
            'huevo_count': 0,
            'chupetin_count': 0,
            'is_qualified': True,
            'group_number': None
        }
        return True
    
    def distribute_candies(self):
        candy_types = ['limon', 'pera', 'huevo']
        for player_name in self.players:
            player = self.players[player_name]
            # Dar 2 caramelos aleatorios
            for _ in range(2):
                candy = random.choice(candy_types)
                player[f'{candy}_count'] += 1
    
    def exchange_candy(self, from_player, to_player, candy_type):
        if from_player not in self.players or to_player not in self.players:
            return False
        if from_player == to_player:
            return False
        
        from_p = self.players[from_player]
        to_p = self.players[to_player]
        
        if from_p[f'{candy_type}_count'] > 0:
            from_p[f'{candy_type}_count'] -= 1
            to_p[f'{candy_type}_count'] += 1
            
            # Registrar intercambio
            self.exchanges.append({
                'from': from_player,
                'to': to_player,
                'candy': candy_type
            })
            return True
        return False
    
    def make_chupetin_phase1(self, player_name, candy_type):
        if player_name not in self.players:
            return False
        
        player = self.players[player_name]
        if player[f'{candy_type}_count'] > 0:
            player[f'{candy_type}_count'] -= 1
            player['chupetin_count'] += 1
            return True
        return False
    
    def make_chupetin_phase2(self, player_name):
        if player_name not in self.players:
            return False
        
        player = self.players[player_name]
        if (player['limon_count'] >= 2 and 
            player['pera_count'] >= 2 and 
            player['huevo_count'] >= 2):
            
            player['limon_count'] -= 2
            player['pera_count'] -= 2
            player['huevo_count'] -= 2
            player['chupetin_count'] += 1
            return True
        return False
    
    def start_phase2(self):
        # Verificar jugadores calificados
        qualified = []
        for player_name, player in self.players.items():
            total_candies = player['limon_count'] + player['pera_count'] + player['huevo_count']
            if player['chupetin_count'] == 0 and total_candies == 0:
                player['is_qualified'] = False
            elif player['chupetin_count'] == 0 and total_candies > 0:
                # Auto-convertir un caramelo
                for candy in ['limon', 'pera', 'huevo']:
                    if player[f'{candy}_count'] > 0:
                        self.make_chupetin_phase1(player_name, candy)
                        break
            
            if player['is_qualified']:
                qualified.append(player_name)
        
        # Dividir en grupos de máximo 10
        if len(qualified) >= 2:
            random.shuffle(qualified)
            mid = min(10, len(qualified) // 2)
            
            for i, player_name in enumerate(qualified):
                group = 1 if i < mid else 2
                self.players[player_name]['group_number'] = group
                
                # Resetear caramelos y dar nuevos
                player = self.players[player_name]
                player['limon_count'] = 0
                player['pera_count'] = 0
                player['huevo_count'] = 0
                
                # Dar 2 caramelos nuevos
                candy_types = ['limon', 'pera', 'huevo']
                for _ in range(2):
                    candy = random.choice(candy_types)
                    player[f'{candy}_count'] += 1
            
            self.status = 'phase2'
            self.phase = 2
            return True
        return False

@app.route('/')
def index():
    global current_game_id
    game = None
    if current_game_id and current_game_id in games_storage:
        game = games_storage[current_game_id]
    
    return render_template('index_simple.html', game=game)

@app.route('/new_game', methods=['POST'])
def new_game():
    global current_game_id
    game = Game()
    games_storage[game.id] = game
    current_game_id = game.id
    flash('Nuevo juego creado', 'success')
    return redirect(url_for('index'))

@app.route('/add_player', methods=['POST'])
def add_player():
    global current_game_id
    name = request.form.get('name', '').strip()
    
    if not name:
        flash('El nombre es requerido', 'error')
        return redirect(url_for('index'))
    
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('index'))
    
    game = games_storage[current_game_id]
    if game.add_player(name):
        flash(f'Jugador {name} agregado', 'success')
    else:
        flash('No se pudo agregar el jugador (límite alcanzado o nombre duplicado)', 'error')
    
    return redirect(url_for('index'))

@app.route('/start_phase1')
def start_phase1():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('index'))
    
    game = games_storage[current_game_id]
    if len(game.players) < 2:
        flash('Se necesitan al menos 2 jugadores', 'error')
        return redirect(url_for('index'))
    
    game.distribute_candies()
    game.status = 'phase1'
    flash('Fase 1 iniciada - ¡Intercambien caramelos!', 'success')
    return redirect(url_for('game'))

@app.route('/game')
def game():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('index'))
    
    game = games_storage[current_game_id]
    if game.status != 'phase1':
        flash('No hay juego activo en Fase 1', 'error')
        return redirect(url_for('index'))
    
    return render_template('game_simple.html', game=game)

@app.route('/exchange_candy', methods=['POST'])
def exchange_candy():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('game'))
    
    game = games_storage[current_game_id]
    from_player = request.form.get('from_player')
    to_player = request.form.get('to_player')
    candy_type = request.form.get('candy_type')
    
    if game.exchange_candy(from_player, to_player, candy_type):
        flash(f'{from_player} intercambió {candy_type} con {to_player}', 'success')
    else:
        flash('No se pudo realizar el intercambio', 'error')
    
    return redirect(url_for('game'))

@app.route('/make_chupetin', methods=['POST'])
def make_chupetin():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('game'))
    
    game = games_storage[current_game_id]
    player_name = request.form.get('player_name')
    candy_type = request.form.get('candy_type')
    
    if game.make_chupetin_phase1(player_name, candy_type):
        flash(f'{player_name} convirtió {candy_type} en chupetín', 'success')
    else:
        flash('No se pudo convertir el caramelo', 'error')
    
    return redirect(url_for('game'))

@app.route('/end_phase1')
def end_phase1():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('index'))
    
    game = games_storage[current_game_id]
    if game.start_phase2():
        flash('Fase 2 iniciada - ¡Ahora se necesitan 2 de cada caramelo para un chupetín!', 'success')
        return redirect(url_for('phase2'))
    else:
        flash('No hay suficientes jugadores calificados para la Fase 2', 'error')
        return redirect(url_for('game'))

@app.route('/phase2')
def phase2():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('index'))
    
    game = games_storage[current_game_id]
    if game.status != 'phase2':
        flash('No hay juego activo en Fase 2', 'error')
        return redirect(url_for('index'))
    
    return render_template('phase2_simple.html', game=game)

@app.route('/make_chupetin_phase2', methods=['POST'])
def make_chupetin_phase2():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('phase2'))
    
    game = games_storage[current_game_id]
    player_name = request.form.get('player_name')
    
    if game.make_chupetin_phase2(player_name):
        flash(f'{player_name} convirtió 6 caramelos en chupetín', 'success')
    else:
        flash('Necesitas 2 de cada tipo de caramelo', 'error')
    
    return redirect(url_for('phase2'))

@app.route('/end_game')
def end_game():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay juego activo', 'error')
        return redirect(url_for('index'))
    
    game = games_storage[current_game_id]
    game.status = 'finished'
    return redirect(url_for('results'))

@app.route('/results')
def results():
    global current_game_id
    if not current_game_id or current_game_id not in games_storage:
        flash('No hay resultados disponibles', 'error')
        return redirect(url_for('index'))
    
    game = games_storage[current_game_id]
    return render_template('results_simple.html', game=game)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)