/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

// Create a new simple document icon component
class SafeDocumentsTypeIcon extends Component {
  static template = xml`
        <div class="o_documents_type_icon">
            <i class="fa fa-file-text-o"/>
        </div>
    `;

  static props = {
    record: { type: Object, optional: true },
    readonly: { type: Boolean, optional: true },
    value: { type: [Boolean, String, Number], optional: true },
  };

  get isRequest() {
    try {
      const record = this.props.record;
      return record && typeof record.isRequest === "function"
        ? record.isRequest()
        : false;
    } catch (error) {
      console.log("isRequest method not available, returning false");
      return false;
    }
  }
}

// Register with a unique name
registry.category("fields").add("safe_documents_type_icon", {
  component: SafeDocumentsTypeIcon,
});

console.log("Safe DocumentsTypeIcon component loaded successfully");
