######################################################
# Permission Order:
# 'a'>'e'>'v'


def permission_value(x):
    """
    This function give permission type 'x' a value in order to represent their order.
    @param x : permission type (e.g. 'v').
    @returns : permission value
    """
    if x is 'v':
        return 1
    elif x is 'e':
        return 2
    elif x is 'a':
        return 3
    else:
        return 0


def permission_max(x, y):
    """
    This function returns maximum permission level of x and y.
    @param x : x permission
    @param y : y permission
    @returns : max permission.
    """
    num_x = permission_value(x)
    num_y = permission_value(y)
    if num_x > num_y:
        return x
    else:
        return y


def permission_min(x, y):
    """
    This function returns minimum permission level of x and y.
    @param x : x permission
    @param y : y permission
    @returns : max permission.
    """
    num_x = permission_value(x)
    num_y = permission_value(y)
    if num_x < num_y:
        return x
    else:
        return y


def permission_entail(x, y):
    """
    This function returns if x permission entails y permission
     (if you have x, does it mean you have y also?)
    @param x : x permission
    @param y : y permission
    @returns : if x permission entails y permission
    """
    num_x = permission_value(x)
    num_y = permission_value(y)
    if num_x >= num_y:
        return True
    else:
        return False
