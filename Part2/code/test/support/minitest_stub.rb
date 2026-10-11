# frozen_string_literal: true

# Minimal stand-in for minitest/mock's Object#stub, which is no longer shipped
# with minitest 6 (it moved to the separate minitest-mock gem). The app code
# never calls this; only the CH01 tests use it to swap the Anthropic client and
# the Turbo broadcaster.
class Object
  def stub(name, val_or_callable)
    method_name = name.to_sym
    singleton   = singleton_class
    had_method  = singleton.method_defined?(method_name) || singleton.private_method_defined?(method_name)
    original    = singleton.instance_method(method_name) if had_method

    singleton.define_method(method_name) do |*args, **kwargs, &blk|
      val_or_callable.respond_to?(:call) ? val_or_callable.call(*args, **kwargs, &blk) : val_or_callable
    end

    yield
  ensure
    if had_method
      singleton.define_method(method_name, original)
    else
      singleton.remove_method(method_name)
    end
  end
end
