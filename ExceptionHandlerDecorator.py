import traceback
from functools import reduce
from typing import Iterable, Optional, Tuple


class ExceptionHandler:
    def __init__(self, return_message: str, log_file: str) -> None:
        self.return_message = return_message
        self.log_file = log_file

    def exception_handler_decorator(
        self,
        exceptions: Tuple[Exception, ...],
        return_message: Optional[str] = None,
        log_file: Optional[str] = None,
    ):
        """Handles all the "exceptions" passed in by catching the error,
            saving the traceback at "log_file" and returning the "return_message"

        Args:
            exception (Tuple[Exception, ...]): tuple of exceptions to be handled
            return_message (str, optional): message that will be returned if exception happens. Defaults to self.return_message
            log_file (str, optional): file to save the traceback. Defaults to self.log_file

        """
        log_file = self.log_file if (log_file is None) else log_file
        return_message = (
            self.return_message if (return_message is None) else return_message
        )

        def decorator(func):
            def wrapper(*args, **kwargs):

                try:
                    return func(*args, **kwargs)
                except exceptions:
                    with open(log_file, "w") as f:
                        traceback.print_exc(file=f)
                    return return_message

            return wrapper

        return decorator


def example() -> None:
    exc_handler = ExceptionHandler(
        return_message="Unexpected error, seek help.",
        log_file="default_error_log.txt",
    )

    # The closer the handler is to the function, the sooner it will try to catch the error.
    # So the order is really important!

    @exc_handler.exception_handler_decorator(exceptions=(Exception,))
    @exc_handler.exception_handler_decorator(
        exceptions=(TypeError,),
        return_message="Type Error ocurred! Please check the data types and try again.",
        log_file="typeerror.txt",
    )
    @exc_handler.exception_handler_decorator(
        exceptions=(ZeroDivisionError,),
        return_message="Division by 0 is impossible!",
        log_file="zerodivisionerror.txt",
    )
    def div_array(num_array: Iterable[float]):
        """[a,b,c] returns a/b/c

        Args:
            num_array (Iterable[float]): iterable of numbers

        """
        return reduce(lambda x, y: x / y, num_array)

    # this is the same as below (but much more practical):

    # try:
    #     div_array([1, 2, 3])
    # except ZeroDivisionError:
    #     save log in specific file and return specific msg
    # except TypeError:
    #     save log in specific file and return specific msg
    # except Exception:
    #     save log in default file and return default msg

    print("No Error:")
    print(div_array([10, 2, 2]))
    print("Error Catched by TypeError:")
    print(div_array(["1", 2]))
    print("Error Catched by ZeroDivisionError:")
    print(div_array([10, 0]))
    print("Error Catched by TypeError:")
    print(div_array(1))


if __name__ == "__main__":
    example()
