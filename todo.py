#!/usr/bin/env python3
'''todo.py
Very basic (unfinished) CLI todo list manager written in Python.
Author: Marcus W. (c0llision)
'''

import sys
import os

TODO_FILE = 'todo.txt'
todo = []


def load_todo():
    ''' load todo list '''
    global todo
    todo = [line.rstrip('\n') for line in open(TODO_FILE, 'r')]


def save_todo():
    ''' save todo list '''
    with open(TODO_FILE, 'w') as f:
        for item in todo:
            f.write("{}\n".format(item))


def action_ls(item=''):
    ''' list tasks into todo list '''
    if not todo:
        print('Nothing todo!')
        return

    for i, line in enumerate(todo):
        print('[{}] {}'.format(i+1, line))


def action_add(item):
    ''' add item to todo list '''
    if not item:
        print('enter item')
        return

    if item in todo:
        print('Task already in todo list')
        return

    todo.append(item)
    print('Added:', item)


def ask_to_delete(**kwargs):
    ''' confirm whether user wishes to delete item '''
    if 'index' in kwargs:
        item = todo[kwargs['index']]
    elif 'line' in kwargs:
        item = kwargs['line']
    else:
        raise Exception('somethings wrong')

    print(item)
    if input('Delete this item? [y/n]: ').lower() == 'y':
        todo.remove(item)


def action_del(item):
    ''' delete a task from the todo list '''
    if not item:
        print('Enter item')
        return

    try:
        index = int(item) - 1
        if index <= len(todo):
            ask_to_delete(index=index)
            return
    except ValueError:
        pass

    for line in todo:
        if item in line:
            ask_to_delete(line=line)
            return
    print('Item not found')


def action_prompt():
    ''' display a prompt that lets user enter cmds '''
    action_ls()

    while True:
        try:
            inp = input('> ').split(' ')
        except KeyboardInterrupt:
            print()
            return

        action, item = inp[0], ' '.join(inp[1:]) if len(inp) > 1 else ''
        do_action(action, item)


def do_action(action, item=''):
    ''' takes action and item and determines which func to call '''
    {
        'ls': action_ls,
        'l': action_ls,
        'add': action_add,
        'del': action_del
    }.get(action, lambda x: print('Invalid action'))(item)


def main():
    ''' main '''
    num_args = len(sys.argv)
    if num_args <= 1:
        action_prompt()
        return

    action, item = sys.argv[1], ' '.join(sys.argv[2:]) if num_args > 2 else ''
    do_action(action, item)


if __name__ == '__main__':
    if os.path.isfile(TODO_FILE):
        load_todo()

    main()
    save_todo()
