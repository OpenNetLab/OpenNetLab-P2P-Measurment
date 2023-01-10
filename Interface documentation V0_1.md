# Interface documentation
## Introduction
In order for your program to be scheduled properly by the OpenNetLab platform, you need to provide the information in the format we specify.
## Required format
The user needs to submit the information to OpenNetLab in the form of a json file, and the following are the required fields of the json configuration file.

- **Number of machines**: only the number of nodes to be called per test
- **Node_N**: information of the node, N is the node number
  - **User-defined-para**: user defined instructions for this node

```python
Example:
{
  Machine = 3
  Node_1
  {
    
    User-defined-para
    {
      Para = {}
    }
  }
  Node_2
  {
    User-defined-para
      { 
        Para = {}
      }
  }
  ...
}

```
