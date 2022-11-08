# __Codeplate__

## Introduction
__Codeplate__ is a simple __template and file structure generator__ that allows you to write templates in the language of the file that you want instead of template language like handlebars. This process is streamlined by the use of 3 major mechanics: __Templates__, __Platters__, and __Plans__. `Templates` are files of any extension where as `Plans` and `Platters` are __json__ files that you can use to build large generators.  

## File Structure
To set up your repo to be used with Codeplate you'll first have to install Codeplate by downloading this repository. (Will have this on pip soon)

You will want to make sure `Codeplate.py` lives at the root folder of your repo.

Next you will want to create a `codeplateconfig.json` in the same location as well as a `Codeplate` directory. Inside the created `Codeplate` directory you should have three more directories labeled `Plans`, `Platters`, and `Templates`.

```
|- root
   |- Codeplate.py
   |- codeplateconfig.json
   |- Codeplate
      |- Plans
      |- Platters
      |- Templates
```  

## Templates
__Files__ that are copied with a newly given __file name__ and __automatically renamed variables__. These should live in the `Templates` directory inside the `Codeplate` directory. Variables that you want to dynamically replace should be prefixed with `codeplate_` as shown in the example below.

#### Example: `BasicComponentTemplate.js`
```js
import React from 'react';

export const codeplate_ComponentName = () => {

  return (
    <h1>
        codeplate_ComponentName
    <h1/>
  )
}

export default codeplate_ComponentName;

```
Now we run this:
```
python3 Codeplate.py tpl BasicComponentTemplate.js answers='{"codeplate_filename": "Button"} filename=Button.js'
```
After we hit enter that's it. We just generated our first template and Button.js should appear in the repo with this content:
```js
import React from 'react';

export const Button = () => {

  return (
    <h1>
        Button
    <h1/>
  )
}

export default Button;

```

###### Note: if something needed is not supplied in the command you will be prompted to input a value for it.

## Platters

Groups of `Template`s represented by a `json` object where the __key:value pair represents a parent/child directory relationship__. With `Platter`s you can very easily generate a common pattern of files like a `README.md`, `*.test.js`, and `*.js` file. These patterns can be referenced later in `Plan`s to generate a LOT of code. These `json` files live in the `Platters` directory of your `Codeplate` directory.

At the root level of the object you will need a key `config` mapped to an Array of strings representing variable names to be replaced __within the `Platter` file__. Any answers passed to Codeplate in the terminal will be mapped to this config array and then the `Platter` will handle the rest.

Only keys of the `Platter` json object and values of the third argument within `Template` arrays will be mapped to.

The anatomy of a `Template` config array is as follows:
``[string, object, object]``

Where `string` in the reference to the template either as the actual file name or an alias in `codeplateconfig.json`, the first `object` is config object, and the second object is mapping of the placeholder variables names in the template file to the strings that will replace them.

#### Example: `FeaturePlatter.json`
##### `BasicComponent.js`
```js
import React from 'react';

export const codeplate_ComponentName = () => {

  return (
    <h1>
        codeplate_ComponentName
    <h1/>
  )
}

export default codeplate_ComponentName;

```
##### `BasicTest.test.js`
```js
import React from 'react';
import {render} from 'react-testing-library';

/** Components */
import codeplate_filename from "codeplate_filename"

test('Default test', () => {
  render(<codeplate_filename/>)
})

```
##### `FeaturePlatter.json`
```json
{
  "config": ["config_filename", "config_testname"],
  "platter": {
    "__test__": {
        "config_testname": ["BasicTest.test.js", {}, {"codeplate_filename": "config_filename"}]
    },
    "config_filename": ["BasicComponent.js", {}, {"codeplate_filename": "config_filename"}]
  }
}
```
Now let's run this platter:
```
python3 Codeplate.py platter BasicFeaturePlatter.js answers='{"config_filename": "Button", "config_testname":"ButtonTest"}'
```
Behind the scenes this is generating a json object that looks like this:
```json
{
  "__test__": {
      "ButtonTest": ["BasicTest.test.js", {}, {"codeplate_filename":"Button"}]
  },
  "Button": ["BasicComponent.js", {}, {"codeplate_filename": "Button"}]
}
```
Which will generate a folder structure that looks like this:
```
|- __test__
  |- ButtonTest.test.js
|- Button.js
```  
## Plans
A json object that uses the key/value system to create massive amounts of code. It takes the structure of the json object and translates it to a directory/file relationship where every nested object is a new directory and non-object values are the contents of the folder. The awesome thing is these values could be `Template`s OR `Platter`s allowing a few lines of code create dozens of files (or as many as you want). This allows you to plan it out visually and afterwards you just run the `Plan` and all the work you put in to map it out automatically generates the whole structure of the new feature. These `json` files live in the `Plans` directory of your `Codeplate` directory.
