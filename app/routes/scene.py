from flask import render_template, redirect, url_for
from app import game_state

def scene(scene):
    game_state['current_scene'] = scene
    
    if scene == 'start':
        return render_template('game_story.html', story="You are standing in front of your house, looking at the neighborhood ranch. Starshine, the horse, is missing. The ranch is owned by a company known for mistreating animals. What will you do?", choices=[
            {'text': 'Visit the Ranch Office', 'route': 'office'},
            {'text': 'Talk to Neighbors', 'route': 'neighbors'},
            {'text': 'Investigate the Stables', 'route': 'stables'}
        ])
    
    elif scene == 'office':
        return render_template('game_story.html', story="You ask about Starshine at the ranch office, but the receptionist is nervous. The manager arrives and warns you to stay out of their business. What will you do?", choices=[
            {'text': 'Ask the Manager Directly', 'route': 'manager_confrontation'},
            {'text': 'Leave and Return Later', 'route': 'start'}
        ])
    
    elif scene == 'neighbors':
        return render_template('game_story.html', story="You ask the neighbors, and one mentions seeing a truck leaving the ranch late at night. It was headed toward the mountains. What will you do?", choices=[
            {'text': 'Follow the Truck\'s Path', 'route': 'mountains'},
            {'text': 'Visit the Local Market', 'route': 'market'}
        ])
    
    elif scene == 'stables':
        return render_template('game_story.html', story="You sneak into the ranch at night and overhear a conversation about selling horses. It looks like something shady is going on. What will you do?", choices=[
            {'text': 'Record the Conversation', 'route': 'record'},
            {'text': 'Confront the Buyers', 'route': 'confront'}
        ])
    
    elif scene == 'manager_confrontation':
        return render_template('game_story.html', story="You confront the manager about Starshine. He gets angry and tells you to leave or face consequences. What will you do?", choices=[
            {'text': 'Leave and Return Later', 'route': 'start'},
            {'text': 'Threaten to Report Them', 'route': 'report'}
        ])
    
    elif scene == 'mountains':
        return render_template('game_story.html', story="You head toward the mountains, following the truck's path. You find a hidden barn. Inside, you spot Starshine. What will you do?", choices=[
            {'text': 'Sneak in at Night', 'route': 'sneak_in'},
            {'text': 'Alert the Authorities', 'route': 'authorities'}
        ])
    
    elif scene == 'sneak_in':
        game_state['rescued'] = True
        return render_template('game_story.html', story="You successfully sneak in and rescue Starshine. You lead her to safety, and the two of you live happily ever after!", choices=[])

    elif scene == 'authorities':
        return render_template('game_story.html', story="You alert the authorities, who raid the ranch and rescue Starshine. The ranch is shut down, and you live happily with Starshine.", choices=[])

    return redirect(url_for('start_game'))