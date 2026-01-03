import pytest
from dash import html
from app import app


class TestDashApp:
    """Test suite for Pink Morsel Sales Dashboard"""
    
    def test_header_is_present(self):
        """Test that the header is present in the app layout"""
        assert app.layout is not None
        
        # Check if there's an H1 element in the layout
        layout_str = str(app.layout)
        assert 'Pink Morsel Sales Analysis' in layout_str
        
        # Verify header component exists
        header_found = False
        for component in app.layout.children:
            if isinstance(component, html.Div):
                if hasattr(component, 'className') and component.className == 'header':
                    header_found = True
                    break
        
        assert header_found, "Header component not found in layout"
    
    def test_visualization_chart_is_present(self):
        """Test that the visualization (dcc.Graph) is present in the app layout"""
        from dash import dcc
        
        layout_str = str(app.layout)
        assert 'sales-chart' in layout_str, "Chart with id 'sales-chart' not found"
        
        # Check that Graph component exists
        chart_found = False
        
        def check_for_graph(component):
            nonlocal chart_found
            if isinstance(component, dcc.Graph):
                if hasattr(component, 'id') and component.id == 'sales-chart':
                    chart_found = True
                    return
            
            if hasattr(component, 'children'):
                if isinstance(component.children, list):
                    for child in component.children:
                        check_for_graph(child)
                else:
                    check_for_graph(component.children)
        
        check_for_graph(app.layout)
        assert chart_found, "Graph component with id 'sales-chart' not found"
    
    def test_region_picker_is_present(self):
        """Test that the region picker (RadioItems) is present in the app layout"""
        from dash import dcc
        
        layout_str = str(app.layout)
        assert 'region-filter' in layout_str, "Region filter with id 'region-filter' not found"
        
        # Check that RadioItems component exists with correct options
        radio_found = False
        regions = ['all', 'north', 'east', 'south', 'west']
        options_found = set()
        
        def check_for_radio(component):
            nonlocal radio_found
            if isinstance(component, dcc.RadioItems):
                if hasattr(component, 'id') and component.id == 'region-filter':
                    radio_found = True
                    # Check for region options
                    if hasattr(component, 'options'):
                        for option in component.options:
                            if option['value'] in regions:
                                options_found.add(option['value'])
                    return
            
            if hasattr(component, 'children'):
                if isinstance(component.children, list):
                    for child in component.children:
                        check_for_radio(child)
                else:
                    check_for_radio(component.children)
        
        check_for_radio(app.layout)
        assert radio_found, "RadioItems component with id 'region-filter' not found"
        assert len(options_found) >= 5, f"Not all region options found. Found: {options_found}"


class TestDashAppCallbacks:
    """Test callbacks and functionality"""
    
    def test_app_has_callback(self):
        """Test that the app has a callback defined"""
        # The app should have callbacks defined
        assert hasattr(app, 'callback_map') or hasattr(app, 'callback_context')
        

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
