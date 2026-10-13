# frozen_string_literal: true

# Minimal stand-in for the anthropic gem so tests never perform network calls.
# It mirrors the parts of the response API the app actually reads:
#   response.content.find { |block| block.type == :tool_use }.input
module FakeAnthropic
  class Block
    attr_reader :type, :input, :text

    def initialize(type:, input: nil, text: nil)
      @type = type
      @input = input
      @text = text
    end
  end

  class Response
    attr_reader :content

    def initialize(blocks)
      @content = blocks
    end
  end

  class Messages
    attr_reader :create_calls

    def initialize(suggestions:)
      @suggestions = suggestions
      @create_calls = []
    end

    def create(**args)
      @create_calls << args
      Response.new([ Block.new(type: :tool_use, input: { "suggestions" => @suggestions }) ])
    end
  end

  # Raises on every call, simulating an unreachable API.
  class FailingMessages
    def create(**_args)
      raise RuntimeError, "simulated API failure"
    end
  end

  class Client
    attr_reader :messages

    def initialize(suggestions: [])
      @messages = Messages.new(suggestions: suggestions)
    end
  end

  class FailingClient
    def initialize(*)
      @messages = FailingMessages.new
    end

    def messages
      @messages
    end
  end

  def self.client(suggestions: [])
    Client.new(suggestions: suggestions)
  end

  def self.failing_client
    FailingClient.new
  end
end
