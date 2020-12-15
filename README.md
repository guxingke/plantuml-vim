# Plantuml-vim

Replace plantuml text code with plantuml server image link or in return.

E.g

````markdown

```plantuml
@startuml
:Hello world;
:This is on defined on
several **lines**;
@enduml
```

````

Replace to 

````markdown

<div hidden>

```plantuml
@startuml
:Hello world;
:This is on defined on
several **lines**;
@enduml
```
<div>

![](https://www.plantuml.com/plantuml/svg/SoWkIImgAStDuNA0iwmyKdDoyXNAyujoKgovh48oCeiLW2W_Jo4bDIqpBpK5oEGgJYrBBKhCKT3IoW4A5MjfMNCvfEQbW4s2q000)
````

## Installation Guide

### Requirements

- vim with python3
- plantuml

### Plugin Installation

* Use Vim Plug (and other manager)

```vim
Plug 'guxingke/plantuml-vim'
```

### Hotkey

```vim
<leander>gg
```

## Demo

![](demo.gif)

