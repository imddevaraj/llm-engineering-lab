from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from registry.prompt_registry import PromptRegistry

class PromptRenderer:
    def __init__(self, registry: 'PromptRegistry'):
        self.registry = registry

    def render(self, template: str, variables: dict):
        rendered = template
        for key, value in variables.items():
            rendered = rendered.replace(f"{{{{{key}}}}}",str(value))
        return rendered

#TO-DO : Simple String replacement on purpose. Needs Templates Engines later (jinja risks, injection, etc..,).