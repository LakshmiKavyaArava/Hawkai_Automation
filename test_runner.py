import os
import sys
import time
from behave import __main__ as behave_executable

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from drivers.driver_setup import get_driver
from config.config import LOGIN_URL, USERNAME, PASSWORD
from pages.login_page import LoginPage
from pages.model_studio_page import ModelStudioPage
from utilities.helper_functions import take_screenshot
import time


def run_complete_flow():
    """
    Test runner that runs both KB and RAG Agent features in sequence
    without closing the browser
    """
    print("=" * 60)
    print("🚀 Starting Complete HawkAI End-to-End Flow")
    print("=" * 60)
    
    # Initialize driver once
    driver = get_driver()
    
    try:
        # ===== LOGIN =====
        print("\n📝 Step 1: Logging in...")
        login_page = LoginPage(driver)
        login_page.open(LOGIN_URL)
        login_page.login(USERNAME, PASSWORD)
        time.sleep(5)
        take_screenshot(driver, "01_Login_Success")
        
        # ===== KNOWLEDGE BASE FLOW =====
        print("\n📚 Step 2: Running Knowledge Base flow...")
        
        # Run KB feature with the same driver
        kb_feature_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "features", 
            "model_studio.feature"
        )
        
        # Pass the driver to behave through environment variable or context
        os.environ['SELENIUM_DRIVER'] = str(id(driver))  # Hacky, but works
        
        # Run KB feature
        kb_result = behave_executable.main([kb_feature_path])
        
        if kb_result != 0:
            print("❌ Knowledge Base flow failed!")
            take_screenshot(driver, "02_KB_Flow_Failed")
        else:
            print("✅ Knowledge Base flow completed successfully!")
            take_screenshot(driver, "02_KB_Flow_Success")
        
        time.sleep(3)
        
        # ===== RAG AGENT FLOW =====
        print("\n🤖 Step 3: Running RAG Agent flow...")
        
        # Run RAG Agent feature with the same driver
        rag_feature_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "features", 
            "rag_agent.feature"
        )
        
        rag_result = behave_executable.main([rag_feature_path])
        
        if rag_result != 0:
            print("❌ RAG Agent flow failed!")
            take_screenshot(driver, "03_RAG_Flow_Failed")
        else:
            print("✅ RAG Agent flow completed successfully!")
            take_screenshot(driver, "03_RAG_Flow_Success")
        
        print("\n" + "=" * 60)
        if kb_result == 0 and rag_result == 0:
            print("🎉 COMPLETE SUCCESS: All flows passed!")
        else:
            print("⚠️ Some flows failed. Check logs above.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during test execution: {str(e)}")
        take_screenshot(driver, "00_Error")
        
    finally:
        # Ask user before closing
        print("\nPress Enter to close browser...")
        input()
        driver.quit()
        print("Browser closed.")


def run_single_feature(feature_name):
    """
    Run a single feature file
    """
    driver = get_driver()
    
    try:
        feature_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "features", 
            feature_name
        )
        
        if not os.path.exists(feature_path):
            print(f"❌ Feature file not found: {feature_path}")
            return
        
        print(f"🚀 Running feature: {feature_name}")
        behave_executable.main([feature_path])
        
    finally:
        print("\nPress Enter to close browser...")
        input()
        driver.quit()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run HawkAI tests')
    parser.add_argument('--flow', choices=['kb', 'rag', 'complete'], 
                       default='complete', help='Which flow to run')
    
    args = parser.parse_args()
    
    if args.flow == 'kb':
        run_single_feature("model_studio.feature")
    elif args.flow == 'rag':
        run_single_feature("rag_agent.feature")
    else:
        run_complete_flow()