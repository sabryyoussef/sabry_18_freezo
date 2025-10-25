from odoo.tests.common import TransactionCase


class TestFreezonerViews(TransactionCase):

    def test_inherited_account_moves_view(self):
        """Test form view for account.move: account.move.inherit.payment.method"""
        view = self.env.ref('freezoner_custom.account_moves')
        self.assertTrue(view, "account_moves view not found")
        self.assertEqual(view.model, 'account.move')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_crm_lead_notes_view(self):
        """Test form view for crm.lead: crm.lead.notes"""
        view = self.env.ref('freezoner_custom.crm_lead_notes')
        self.assertTrue(view, "crm_lead_notes view not found")
        self.assertEqual(view.model, 'crm.lead')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_document_form_view_view(self):
        """Test form view for documents.document: documents.document.form"""
        view = self.env.ref('freezoner_custom.document_form_view')
        self.assertTrue(view, "document_form_view view not found")
        self.assertEqual(view.model, 'documents.document')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_documents_request_wizard_forms_view(self):
        """Test form view for documents.request_wizard: documents.request_wizard"""
        view = self.env.ref('freezoner_custom.documents_request_wizard_forms')
        self.assertTrue(view, "documents_request_wizard_forms view not found")
        self.assertEqual(view.model, 'documents.request_wizard')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_share_view_form_new_popup_view(self):
        """Test form view for documents.share: Share Document"""
        view = self.env.ref('freezoner_custom.share_view_form_new_popup')
        self.assertTrue(view, "share_view_form_new_popup view not found")
        self.assertEqual(view.model, 'documents.share')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_share_view_form_view(self):
        """Test form view for documents.share: documents.share.form"""
        view = self.env.ref('freezoner_custom.share_view_form')
        self.assertTrue(view, "share_view_form view not found")
        self.assertEqual(view.model, 'documents.share')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_product_product_responsible_view(self):
        """Test form view for product.product: product.product.responsible"""
        view = self.env.ref('freezoner_custom.product_product_responsible')
        self.assertTrue(view, "product_product_responsible view not found")
        self.assertEqual(view.model, 'product.product')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_product_template_document_type_view(self):
        """Test form view for product.template: product.template.document.type"""
        view = self.env.ref('freezoner_custom.product_template_document_type')
        self.assertTrue(view, "product_template_document_type view not found")
        self.assertEqual(view.model, 'product.template')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_projects_project_view(self):
        """Test form view for project.project: project.project"""
        view = self.env.ref('freezoner_custom.projects_project')
        self.assertTrue(view, "projects_project view not found")
        self.assertEqual(view.model, 'project.project')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_project_search_view(self):
        """Test search view for project.project: project.search"""
        view = self.env.ref('freezoner_custom.project_search')
        self.assertTrue(view, "project_search view not found")
        self.assertEqual(view.model, 'project.project')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_project_stages_kanban_view(self):
        """Test kanban view for project.project: project_stages_kanban"""
        view = self.env.ref('freezoner_custom.project_stages_kanban')
        self.assertTrue(view, "project_stages_kanban view not found")
        self.assertEqual(view.model, 'project.project')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_project_subtask_tree_view(self):
        """Test list view for project.task: project.subtask.tree"""
        view = self.env.ref('freezoner_custom.project_subtask_tree')
        self.assertTrue(view, "project_subtask_tree view not found")
        self.assertEqual(view.model, 'project.task')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_project_task_document_view(self):
        """Test form view for project.task: project.task"""
        view = self.env.ref('freezoner_custom.project_task_document')
        self.assertTrue(view, "project_task_document view not found")
        self.assertEqual(view.model, 'project.task')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_project_task_product_view(self):
        """Test form view for project.task: project.task.product"""
        view = self.env.ref('freezoner_custom.project_task_product')
        self.assertTrue(view, "project_task_product view not found")
        self.assertEqual(view.model, 'project.task')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_view_task_kanban_inherit_my_task_view(self):
        """Test kanban view for project.task: task_client_kanban"""
        view = self.env.ref('freezoner_custom.view_task_kanban_inherit_my_task')
        self.assertTrue(view, "view_task_kanban_inherit_my_task view not found")
        self.assertEqual(view.model, 'project.task')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_project_task_assignees_form_view_view(self):
        """Test form view for project.task.assignees: project.task.assignees.form.view"""
        view = self.env.ref('freezoner_custom.project_task_assignees_form_view')
        self.assertTrue(view, "project_task_assignees_form_view view not found")
        self.assertEqual(view.model, 'project.task.assignees')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_project_task_type_stages_view(self):
        """Test form view for project.task.type: project.task.type"""
        view = self.env.ref('freezoner_custom.project_task_type_stages')
        self.assertTrue(view, "project_task_type_stages view not found")
        self.assertEqual(view.model, 'project.task.type')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_project_update_fields_form_view_view(self):
        """Test form view for project.update.fields: project.update.fields.form.view"""
        view = self.env.ref('freezoner_custom.project_update_fields_form_view')
        self.assertTrue(view, "project_update_fields_form_view view not found")
        self.assertEqual(view.model, 'project.update.fields')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_rating_form_view(self):
        """Test list view for rating.rating: rating.form"""
        view = self.env.ref('freezoner_custom.rating_form')
        self.assertTrue(view, "rating_form view not found")
        self.assertEqual(view.model, 'rating.rating')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_remarks_wizard_form_view_view(self):
        """Test form view for remarks.wizard: remarks.wizard.form.view"""
        view = self.env.ref('freezoner_custom.remarks_wizard_form_view')
        self.assertTrue(view, "remarks_wizard_form_view view not found")
        self.assertEqual(view.model, 'remarks.wizard')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_project_required_documents_wizard_form_view_view(self):
        """Test form view for required.documents.wizard: required.documents.wizard.form.view"""
        view = self.env.ref('freezoner_custom.project_required_documents_wizard_form_view')
        self.assertTrue(view, "project_required_documents_wizard_form_view view not found")
        self.assertEqual(view.model, 'required.documents.wizard')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_partner_products_view(self):
        """Test form view for res.partner: res.partner.products.from"""
        view = self.env.ref('freezoner_custom.partner_products')
        self.assertTrue(view, "partner_products view not found")
        self.assertEqual(view.model, 'res.partner')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_project_return_form_view_view(self):
        """Test form view for return.project.wizard: return.project.wizard.form.view"""
        view = self.env.ref('freezoner_custom.project_return_form_view')
        self.assertTrue(view, "project_return_form_view view not found")
        self.assertEqual(view.model, 'return.project.wizard')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_sale_crm_wizard_form_view_view(self):
        """Test form view for sale.crm.wizard: sale.crm.wizard.form.view"""
        view = self.env.ref('freezoner_custom.sale_crm_wizard_form_view')
        self.assertTrue(view, "sale_crm_wizard_form_view view not found")
        self.assertEqual(view.model, 'sale.crm.wizard')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_sale_view_quotation_tree_with_onboardin_view(self):
        """Test list view for sale.order: sale.order"""
        view = self.env.ref('freezoner_custom.sale_view_quotation_tree_with_onboardin')
        self.assertTrue(view, "sale_view_quotation_tree_with_onboardin view not found")
        self.assertEqual(view.model, 'sale.order')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_sale_order_form_view_inherit_view(self):
        """Test form view for sale.order: sale.order.form.inherit"""
        view = self.env.ref('freezoner_custom.sale_order_form_view_inherit')
        self.assertTrue(view, "sale_order_form_view_inherit view not found")
        self.assertEqual(view.model, 'sale.order')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_task_next_wizard_form_view_view(self):
        """Test form view for task.next.wizard: task.next.wizard.form.view"""
        view = self.env.ref('freezoner_custom.task_next_wizard_form_view')
        self.assertTrue(view, "task_next_wizard_form_view view not found")
        self.assertEqual(view.model, 'task.next.wizard')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_task_wizard_form_view_view(self):
        """Test form view for task.wizard: task.wizard.form.view"""
        view = self.env.ref('freezoner_custom.task_wizard_form_view')
        self.assertTrue(view, "task_wizard_form_view view not found")
        self.assertEqual(view.model, 'task.wizard')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")

    def test_inherited_sale_order_portal_template_thread_hide_view(self):
        """Test qweb view for None: sale_order_portal_template_thread_hide"""
        view = self.env.ref('freezoner_custom.sale_order_portal_template_thread_hide')
        self.assertTrue(view, "sale_order_portal_template_thread_hide view not found")
        self.assertEqual(view.model, 'None')
        # Test that view architecture can be read
        arch = self.env['ir.ui.view'].browse(view.id).read_combined(['arch'])
        self.assertTrue(arch, "View architecture could not be read")
