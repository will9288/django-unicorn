import { contains } from "./utils.js";

/**
 * Encapsulate DOM element attribute for Unicorn-related information.
 */
export class Attribute {
  constructor(attribute) {
    this.attribute = attribute;
    this.name = this.attribute.name;
    this.value = this.attribute.value;
    this.isUnicorn = false;
    this.isModel = false;
    this.isField = false;
    this.isPoll = false;
    this.isKey = false;
    this.isPK = false;
    this.isError = false;
    this.modifiers = {};
    this.eventType = null;

    this.init();
  }

  /**
   * Init the attribute.
   */
  init() {
    if (this.name.startsWith("unicorn:") || this.name.startsWith("u:")) {
      this.isUnicorn = true;

      // Use `contains` when there could be modifiers
      if (contains(this.name, ":model")) {
        this.isModel = true;
      } else if (contains(this.name, ":field")) {
        this.isField = true;
      } else if (contains(this.name, ":db")) {
        this.isDb = true;
      } else if (contains(this.name, ":poll")) {
        this.isPoll = true;
      } else if (this.name === "unicorn:key" || this.name === "u:key") {
        this.isKey = true;
      } else if (this.name === "unicorn:pk" || this.name === "u:pk") {
        this.isPK = true;
      } else if (contains(this.name, ":error:")) {
        this.isError = true;
      } else {
        const actionEventType = this.name.replace("unicorn:", "").replace("u:", "");

        if (
          actionEventType !== "id" &&
          actionEventType !== "name" &&
          actionEventType !== "checksum"
        ) {
          this.eventType = actionEventType;
        }
      }

      let potentialModifiers = this.name;

      if (this.eventType) {
        potentialModifiers = this.eventType;
      }

      // Find modifiers and any potential arguments
      potentialModifiers
        .split(".")
        .slice(1)
        .forEach((modifier) => {
          const modifierArgs = modifier.split("-");
          this.modifiers[modifierArgs[0]] =
            modifierArgs.length > 1 ? modifierArgs[1] : true;

          // Remove any modifier from the event type
          if (this.eventType) {
            this.eventType = this.eventType.replace(`.${modifier}`, "");
          }
        });
    }
  }
}
