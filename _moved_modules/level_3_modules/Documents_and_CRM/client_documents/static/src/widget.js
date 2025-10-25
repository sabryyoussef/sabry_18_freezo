/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class Many2ManyPdfPreview extends Component {
  static template = "client_documents.Many2ManyPdfPreview";

  setup() {
    this.state = useState({
      attachments: this.props.record?.data?.pdf_files?.res_ids || [],
    });
  }

  async renderPdfPreviews() {
    const attachments = this.state.attachments;
    for (const attachmentId of attachments) {
      // Fetch the attachment using attachmentId and render preview
      // Use PDF.js or any other library to render the preview
    }
  }

  mounted() {
    this.renderPdfPreviews();
  }
}

registry.category("view_widgets").add("many2many_pdf_preview", {
  component: Many2ManyPdfPreview,
});
