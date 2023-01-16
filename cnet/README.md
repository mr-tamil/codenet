```html
While Edit: Consider to Modify Repo
    : .README.md
    :  all.py
    :  __init__.py
```



## Format
```python
from cnet.all import *


# install packages
install_package('pandas')
install_packages(['pandas','numpy'])

# import modules
import_module(globals(),module='dill.source', install=True)
import_modules(globals(), modules=['pandas', ('dill.source','dillsource'), ('numpy', 'np')], install=True)
# impfilelib(globals(), filepath='req.txt')
onelib(globals(), project='default')


# class ::
class Person:

    # selfit decorator
    @selfit
    def __init__(self, name, age, work):

        # setattrs method
        setattrs(self, locals())
        setattrs(self, name=name, age=age,profession=work)


    # selfit decorator
    @selfit.adjust
    @selfit.adjust(self=True, default=None)
    def change(self, *args, **kwargs):
        pass


if __name__ == "__main__":
    result = Person('Dinesh', 21, 'Mech')

    # objectize
    obj1 = Objectize.list(['name', 'age'], ['Dinesh', 21])
    obj2 = Objectize.dict({'name': 'age', 'Dinesh': 21})
    print(obj1.__dict__)

    # preaty print
    pprint({'name': 'age', 'Dinesh': 21})

    # json print
    jprint({'name': 'age', 'Dinesh': 21})
    
    # tuple instantiate
    ins1 = TupleInstantiate.list(['name', 'age'], ['Dinesh', 21])
    ins2 = TupleInstantiate.dict({'name': 'age', 'Dinesh': 21})
    print(ins1.name, ins1[1])

    # class function positional (actual) name
    print(cfpname(result))
    print(cfpname(result.change))

    # print, enable, disable
    prints.enable()
    prints.enable()
    with prints(state=False):
        ''' will print or don't print'''



```
