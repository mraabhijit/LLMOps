import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate

from config import PROMPTS_DIR


class PromptRegistry:
    def __init__(self, prompts_dir: Path | str = Path(PROMPTS_DIR)):
        self.prompts_dir = Path(prompts_dir)
        self._manifest = self.prompts_dir / "manifest.json"

    @property
    def manifest(self):
        return self._manifest

    def register(
        self,
        name: str,
        version: str,
        filepath: Path | str,
        description: str,
        author: str,
    ):
        filepath = Path(filepath)
        if not (self.prompts_dir / filepath).exists():
            raise FileNotFoundError(f"{filepath.absolute()} not found.")

        prompt_version = {
            "filepath": filepath.name,
            "description": description,
            "author": author,
            "created_at": datetime.now(UTC).isoformat(),
            "is_active": True,
        }

        if not self.manifest.exists():
            content = {"prompts": {name: {"versions": {version: prompt_version}}}}

            with open(self.manifest, "w") as f_out:
                json.dump(content, f_out, indent=2)
            return

        with open(self.manifest, "r") as f_in:
            existing_prompts = json.load(f_in)

        recipes = existing_prompts.get("prompts", {})
        if name not in recipes:
            existing_prompts["prompts"][name] = {"versions": {version: prompt_version}}

        else:
            if version in recipes[name]["versions"]:
                raise ValueError(f"Version: {version} already exists.")

            for info in recipes[name]["versions"].values():
                info["is_active"] = False

            existing_prompts["prompts"][name]["versions"][version] = prompt_version

        with open(self.manifest, "w") as f_out:
            json.dump(existing_prompts, f_out, indent=2)
        print(f"Registered {name} {version}")

    def get_prompt(
        self,
        name: str,
        version: Optional[str] = None,
    ) -> ChatPromptTemplate:
        prompts_register = self._validate()
        prompts = prompts_register["prompts"]

        if name not in prompts:
            raise ValueError(f"{name} not found in {self.manifest}.")

        prompt_filepath = ""
        if version and version not in prompts[name]["versions"]:
            raise ValueError(f"{version} not found in {self.manifest}.")
        elif version:
            prompt_filepath = prompts[name]["versions"][version]["filepath"]
        else:
            for val in prompts[name]["versions"].values():
                if val["is_active"]:
                    prompt_filepath = val["filepath"]
                    break

        prompt_file = self.prompts_dir / prompt_filepath
        if not prompt_file.exists():
            raise FileNotFoundError(f"{prompt_file.absolute()} not found.")

        with open(prompt_file, "r") as f_in:
            template = f_in.read()

        return ChatPromptTemplate.from_template(template=template)

    def set_active(
        self,
        name: str,
        version: str,
    ):
        prompts_register = self._validate()
        prompts = prompts_register["prompts"]

        if name not in prompts:
            raise ValueError(f"{name} not found in {self.manifest}.")

        if version and version not in prompts[name]["versions"]:
            raise ValueError(f"{version} not found in {self.manifest}.")

        for k, v in prompts[name]["versions"].items():
            if k != version:
                v["is_active"] = False
            else:
                v["is_active"] = True

        with open(self.manifest, "w") as f_out:
            json.dump(prompts_register, f_out, indent=2)
        print(f"Active version set to: {version}")

    def list_versions(self, name: str) -> list[dict]:
        prompts_register = self._validate()
        prompts = prompts_register["prompts"]

        if name not in prompts:
            raise ValueError(f"{name} not found in {self.manifest}.")

        return [{"version": k, **v} for k, v in prompts[name]["versions"].items()]

    def compare(
        self,
        name: str,
        version_a: str,
        version_b: str,
    ) -> dict:
        prompts_register = self._validate()
        prompts = prompts_register["prompts"]

        if name not in prompts:
            raise ValueError(f"{name} not found in {self.manifest}.")

        if version_a and version_a not in prompts[name]["versions"]:
            raise ValueError(f"{version_a} not found in {self.manifest}.")

        if version_b and version_b not in prompts[name]["versions"]:
            raise ValueError(f"{version_b} not found in {self.manifest}.")

        prompt_dict = {}
        for version in [version_a, version_b]:
            file = prompts[name]["versions"][version]["filepath"]

            with open((self.prompts_dir / file), "r") as f_in:
                prompt_dict[version] = f_in.read()

        return prompt_dict

    def _validate(
        self,
    ) -> dict:
        if not self.manifest.exists():
            raise FileNotFoundError(f"{self.manifest.absolute()} not found.")

        with open(self.manifest, "r") as f_in:
            prompts_register = json.load(f_in)

        return prompts_register
