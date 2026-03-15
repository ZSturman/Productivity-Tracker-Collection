//
//  InputVM.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/30/23.
//

import Foundation
import SwiftUI

class InputVM: ObservableObject {
    @Published var input: Input
    
    init(existingInput: Input? = nil, inputType: InputType = .SetText) {
        if let providedInput = existingInput {
            self.input = providedInput
        } else {
            // Assuming the Trigger class has a constructor that accepts type: TriggerType
            self.input = Input(type: inputType)
        }
    }
    
}

