//
//  Input.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/17/23.
//


import Foundation
import CoreData

class Input: NSManagedObject {
    @NSManaged var id: UUID
    @NSManaged var title: String
    @NSManaged var systemImage: String
    @NSManaged var inputType: String
    @NSManaged var isFirst: Bool
    @NSManaged var orderIndex: Int16
    @NSManaged var dateUpdated: Date
    
    @NSManaged public var actionState: ActionState?
    @NSManaged public var parentTrigger: Trigger?
    @NSManaged public var nextInput: Input?
    @NSManaged public var previousInput: Input?
    @NSManaged public var records: NSSet
    
    override func awakeFromInsert() {
        super.awakeFromInsert()
        
        setPrimitiveValue(UUID(), forKey: "id")
        setPrimitiveValue(false, forKey: "isFirst")
        setPrimitiveValue(Date.now, forKey: "dateUpdated")
    }
}

enum InputType: String {
    case askForTextInput = "AskForTextInput"
    case askForNumberInput = "AskForNumberInput"
    case setTextInput = "SetTextInput"
    case setNumberInput = "SetNumberInput"
    case calculationInput = "CalculationInput"
}



final class SetTextInput: Input {
    @NSManaged var outputValue: String
    
    override func awakeFromInsert() {
        super.awakeFromInsert()
        self.inputType = InputType.setTextInput.rawValue
    }
}

final class SetNumberInput: Input {
    @NSManaged var outputValue: Double
    
    override func awakeFromInsert() {
        super.awakeFromInsert()
        self.inputType = InputType.setNumberInput.rawValue
    }
}

final class CalculateInput: Input {
    @NSManaged var operation: String
    @NSManaged var outputValue: Double

    override func awakeFromInsert() {
        super.awakeFromInsert()
        self.inputType = InputType.calculationInput.rawValue
    }
}

class AskForTemplate: Input {
    @NSManaged var providePrompt: Bool
    @NSManaged var prompt: String?
    @NSManaged var provideDefault: Bool
    @NSManaged var allowBlank: Bool

    override func awakeFromInsert() {
        super.awakeFromInsert()
        // Here, we don't set inputType since this is a generic template class.
        setPrimitiveValue(false, forKey: "providePrompt")
        setPrimitiveValue(true, forKey: "allowBlank")
        setPrimitiveValue(false, forKey: "provideDefault")
    }
}

final class AskForTextInput: AskForTemplate, Identifiable {
    @NSManaged var defaultValue: String?
    @NSManaged var outputValue: String

    override func awakeFromInsert() {
        super.awakeFromInsert()
        self.inputType = InputType.askForTextInput.rawValue
    }
}

final class AskForNumberInput: AskForTemplate, Identifiable {
    @NSManaged var allowDecimals: Bool
    @NSManaged var allowNegatives: Bool
    @NSManaged var defaultValue: Double
    @NSManaged var outputValue: Double

    override func awakeFromInsert() {
        super.awakeFromInsert()
        self.inputType = InputType.askForNumberInput.rawValue
        setPrimitiveValue(false, forKey: "allowDecimals")
        setPrimitiveValue(true, forKey: "allowNegatives")
        setPrimitiveValue(0.0, forKey: "defaultValue")
    }
}

