from unittest.mock import patch, MagicMock
from structured_agent import generate_code_with_structured_output

@patch("structured_agent.client.chat.completions.create")
def test_auto_retry(mock_create):
    bad_response = MagicMock()
    bad_response.choices[0].message.content = '{"code": "print(1)"}' 
    
    good_response = MagicMock()
    good_response.choices[0].message.content = '{"code": "print(1)", "language": "python", "explanation": "test"}'
    
    mock_create.side_effect = [bad_response, good_response]
    
    print("Starting mock test...")
    generate_code_with_structured_output()
    print("Test completed successfully!")

if __name__ == "__main__":
    test_auto_retry()