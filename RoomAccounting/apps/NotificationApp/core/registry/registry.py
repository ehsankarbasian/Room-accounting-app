from typing import Dict, Type, Optional, Callable


def make_registry() -> tuple[Dict[str, Type], Callable]:
    
    REGISTRY: Dict[str, Type] = {}

    def decorator_to_register(_cls=None, *, name: Optional[str] = None):
        
        def decorator(cls: Type):
            
            key = name or cls.__name__
            
            if key in REGISTRY:
                raise RuntimeError(f"{key!r} already registered")
            
            REGISTRY[key] = cls
            return cls

        if _cls is None:
            return decorator
        
        return decorator(_cls)

    return REGISTRY, decorator_to_register
