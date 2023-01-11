# Wolf
Wolf is a Work on less flow of codes to ease of work.

Reverse letters of Wolf is floW and bbbreviation is 'Flow of Work'.

It has 4 main features,
   1. Neurons
   2. Works
   3. Flow
   4. CodeFlow


## Code Example 
```python
# working class and functions 
def adding(): pass
def removing(): pass
class printing: pass
```

### 1. Neurons
```python
from wolf import Neurons

# initialise
nf = Neurons(globals())

# add
nf.add(adding)
nf.add(printing, 'printing')
nf + removing 


# remove
nf.remove('printing')

# show
print(nf)
print(nf.show("adding"))
print(nf.show_classes())
print(nf.show_functions())

# get
print(nf.get_list(complete=True))
print(nf.get_classes)
print(nf.get_functions)
print(nf.getins("adding"))


```

### 2. Works
##### Create
```python
from wolf import Works

# initialise 
nlp = Works("NLP", nf)
obj = nlp.objects()

# access objects
print(obj)

# add, remove neurons from Works
nlp.add(Neurons, "Neurone")
nlp.remove("Neurone")

# save
nlp.save("Project.pwf")

# add new work
glp = Works("GLP", nf)
glp.save_all("Project.pwf")

```
##### Retrieve
```python
# initialise
from wolf import Works
works = Works("Project.pwf")
nlp = works("NLP", delete= False)
obj = nlp.objects()
print(obj)

# add new neuron and remove old neuron 
nlp.add(Neurons, "Neurone")
nlp.removing("Neurone")

```


### 3. Flow
class objects must have __call__ method and return function.

function objects must have one input parameter and return function.

This __Flow__ feature is a low level work flow technique to ease the work.

__Flow__ works well if we only use functions only techniques.
```
Note:
    1. Create input, output, functions and  classes universal format, style and techniques.
    2. Use flow format.
```

```python
from wolf import Flow

# initialise
flow = Flow(nf)
flow("adding > removing > printing")
ins = flow.fit()

# get
print(ins([[10]]))

```
#### FLow Format
```python
# input format: parameter
input = [args, kwargs]

# output format: return
output = [args, kwargs]

# function format: def
def function_name(input):
    '''set args and kwargs default value'''
    '''extract parameters from input'''
    '''do statements'''
    output = [args, kwargs]
    return output

# class format: class
class class_name:
    '''do methods'''
    def __call__(self, input):
        '''set args and kwargs default value'''
        '''extract parameters from input'''
        '''do statements'''
        output = [args, kwargs]
        return output
```

### 4. Code Flow
```python
from wolf import CodeFlow

# initialise 
wf = CodeFlow(globals(), neglect= ['class', "function"])

# show
wf()
wf('class')
```

## Modules and Objects: Device Compatibility or Restrinctions
```
Works :: POSIX
Neurons.save :: POSIX
Neurons.saving :: POSIX
```
## Modules and Objects: Device Not Compatibility or Restrinctions
```
Flow.show_logs :: ColabNB
```
