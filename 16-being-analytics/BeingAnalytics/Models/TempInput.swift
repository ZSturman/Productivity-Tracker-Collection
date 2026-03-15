//
//  TempInputNew.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/7/23.
//

import CoreData
import SwiftUI

struct TempInput: Hashable, Identifiable {
    var id: UUID = UUID()
    var inputType: InputTypeOptions
    var order: Int = 0
    var nextInput: UUID? = nil
    var previousInput: UUID? = nil
    var inCalculation: Bool = false
    var calculationInputID: UUID? = nil
    

    // Computed properties based on the inputType
    var title: InputTypeOptions.RawValue {
        return inputType.rawValue
    }
    
    var userActionRequired: Bool {
        return inputType.userActionRequired
    }
    
    var inputRowExpanded: Bool {
        return inputType.rowExpanded
    }
    
    var inputSystemImage: String {
        return inputType.inputSystemImage
    }
    
    var triggerOutputDatetime: String {
        return FormattingHelper.shortenDateWithYear(Date())
    }
    var triggerOutputDate: String {
        return FormattingHelper.shortenDate(Date())
    }
    var triggerOutputTime: String {
        return FormattingHelper.formatTime(Date())
    }
    
    var inputOutput: String {
        switch inputType {
        case .askForText:
            if defaultBool {
                return defaultString
            } else {
                return "Text"
            }
        case .askForNumber:
            return FormattingHelper.formatNumber(defaultNumberValue)
           
        case .currentDatetime:
            if date == false && time == false {
                return ""
            } else if date == true && time == true {
                return triggerOutputDatetime
            } else if date == true && time == false {
                return triggerOutputDate
            } else if date == false && time == true{
                return triggerOutputTime
            } else {
                return triggerOutputDatetime
            }
            
        case .getLocation:
            return ""
        case .setText:
            return setValue
        case .setNumber:
            return String(numberValue)
        case .calculate:
            return String(numberValue)
            
        }
    }
    
    // TempInputAskForNumberTemplate properties
    var allowDecimals: Bool = false
    var allowNegatives: Bool = false
    var currency: Bool = false
    var promptBool: Bool = false
    var promptString: String = ""
    var useRange: Bool = false

    // TempInputAskForText properties
    var allowBlank: Bool = true
    var defaultBool: Bool = false
    var defaultString: String = ""

    // TempInputAskForNumberDouble properties
    var defaultNumberValue: Double = 0.0
    var maxNumberValue: Double = 100.0
    var minNumberValue: Double = 0.0
    var stepCount: Double = 1.0

    // CurrentDatetimeParameters properties
    var date: Bool = true
    var time: Bool = true

    // SetTextParameters properties
    var setValue: String = ""

    // SetNumberParameters properties
    var decimal: Bool = false
    
    var datetimeValue: Date = Date()

    // SetNumberDoubleParameters properties
    var numberValue: Double = 0.0
    
    // Calculate parameters
    var calculateOperation: Operation = .addition
    var calculationDateOrTime: DateOrTime = .both
    var calculationOutputType: NumberType = .integer
    var valueOne: Double? = 20
    var valueTwo: Double? = 10
    
    var selectedInputOne: UUID? = nil
    var valueOneIsInput: Bool {
        if selectedInputOne != nil {
            return true
        } else {
            return false
        }
    }
    
    var selectedInputTwo: UUID? = nil
    var valueTwoIsInput: Bool {
        if selectedInputTwo != nil {
            return true
        } else {
            return false
        }
    }
    
    var calculationType: CalculationType = .number
    
    init(id: UUID = UUID(), inputType: InputTypeOptions, order: Int = 0, nextInput: UUID? = nil, previousInput: UUID? = nil) {
        self.id = id
        self.inputType = inputType
        self.order = order
        self.nextInput = nextInput
        self.previousInput = previousInput
    }
}



enum InputTypeOptions: String, CaseIterable {
    case askForNumber = "Ask for number"
    case askForText = "Ask for text"
    case currentDatetime = "Get current datetime"
    case getLocation = "Get current location"
    case setText = "Set text"
    case setNumber = "Set number"
    case calculate = "Calculate"
//    case setGlobalVariable = "Set global variable"
//    case getGlobalVariable = "Get global variable"
//    case setLocalVariable = "Set local variable"
//    case getLocalVariable = "Get local variable"
    

    var inputTypeName: String {
        return self.rawValue
    }
    
    var inputSystemImage: String {
        switch self {
        case .askForText:
            return "textformat"
        case .askForNumber:
            return "number"
        case .currentDatetime:
            return "calendar.badge.clock"
        case .getLocation:
            return "location.circle"
        case .setText:
            return "square.and.pencil"
        case .setNumber:
            return "number.square"
        case .calculate:
            return "plus.forwardslash.minus"
            
        }
    }
    
    var numberCalculation: Bool {
        switch self {
        case .askForText, .currentDatetime, .getLocation, .setText:
            return false
        case .askForNumber, .setNumber, .calculate:
            return true
        }
    }
    
    var dateCalculation: Bool {
        switch self {
        case .askForText, .getLocation, .setText, .askForNumber, .setNumber:
            return false
        case .currentDatetime, .calculate:
            return true
        }
    }
    



    var userActionRequired: Bool {
        switch self {
        case .askForText, .askForNumber:
            return true
        case .currentDatetime, .getLocation, .setText, .setNumber, .calculate:
            return false
        }
    }
    
    var rowExpanded: Bool {
        switch self {
        case .askForText, .askForNumber, .setText, .setNumber, .calculate:
            return true
        case .currentDatetime, .getLocation:
            return false
        }
    }
    
    var inputDescription: String {
        switch self {
        case .askForText:
            return "Ask user for text input"
        case .askForNumber:
            return "Ask user for number input"
        case .currentDatetime:
            return "Retrieve the current date and time"
        case .getLocation:
            return "Retrieve the user's current location"
        case .setText:
            return "Set a specific text value"
        case .setNumber:
            return "Set a specific number value"
        case .calculate:
            return "Perform a calculation"
//        case .setGlobalVariable:
//            return "Store a value that persists across executions"
//        case .getGlobalVariable:
//            return "Retrieve a value that persists across executions"
//        case .setLocalVariable:
//            return "Store a value just for the duration of the current trigger"
//        case .getLocalVariable:
//            return "Retrieve a value set within the current trigger"
        }
    }

}


// MARK: - Constants
enum CalculationType: String, CaseIterable {
    case number = "Number"
    case datetime = "Datetime"
}

enum Operation: String, CaseIterable {
    case addition = "+"
    case subtraction = "-"
    case multiplication = "x"
    case division = "/"
}

enum NumberType: String, CaseIterable {
    case integer = "Integer"
    case decimal = "Decimal"
    case currency = "Currency"
}

enum DateOrTime: String, CaseIterable {
    case date = "Date"
    case time = "Time"
    case both = "Both"
}


// MARK: - Initializing TempInput from Input
extension TempInput {
    // Initialize TempInput from an existing CoreData Input object
    init(from input: Input) {
        // Here, map the properties of the Input entity to the properties of TempInput
        // For example:
        self.id = input.id ?? UUID() // Provide a default value
        self.inputType = InputTypeOptions(rawValue: input.inputType ?? "") ?? .askForText
        let order = Int(input.order)
        self.order = order
        
        switch self.inputType {
        case .askForText:
            print("ASK FOR TEXT")
        case .askForNumber:
            if let specificSelf = input as? InputAskForNumber {
                
                self.allowDecimals = specificSelf.allowDecimals
                self.allowNegatives = specificSelf.allowNegatives
                self.currency = specificSelf.currency
                self.promptBool = specificSelf.promptBool
                self.promptString = specificSelf.promptString ?? ""
                self.useRange = specificSelf.useRange
                self.defaultNumberValue = specificSelf.defaultValue
                self.maxNumberValue = specificSelf.maxValue
                self.minNumberValue = specificSelf.minValue
                self.stepCount = specificSelf.stepCount
            }
        case .calculate:
            print("CALCULATE")
        case .currentDatetime:
            print("CURRENT DATETIMNE")
        case .getLocation:
            print("LOCATION")
        case .setNumber:
            print("SET NUMBER")
        case .setText:
            print("SET TEXT")
            
        }
        
    }
}





// MARK: - Initializing Input from TempInput
extension Input {
    // Initialize CoreData Input object from a TempInput object
    convenience init(from tempObject: TempInput, in context: NSManagedObjectContext) {
        
        // Determine the entity name based on inputType
        let entityName: String
        switch tempObject.inputType {
        case .askForText:
            entityName = "InputAskForText"
        // Add more cases for other input types as needed
        default:
            entityName = "Input" // Fallback to the parent entity or another default
        }
        
        // Retrieve the entity description based on determined entity name and initialize
        guard let entity = NSEntityDescription.entity(forEntityName: entityName, in: context) else {
            fatalError("Failed to initialize \(entityName) entity.")
        }
        self.init(entity: entity, insertInto: context)
        
        // Assign common properties from the temporary object
        self.id = tempObject.id
        self.inputType = tempObject.inputType.rawValue
        self.title = tempObject.title
        let order = Int32(tempObject.order)
        self.order = order
        self.userActionRequired = tempObject.userActionRequired
        
        // Assign specific properties for different child entities
        switch tempObject.inputType {
        case .askForText:
            if let specificSelf = self as? InputAskForText {
                specificSelf.allowBlank = tempObject.allowBlank
                // Assign other properties specific to InputAskForText
            }
        case .askForNumber:
            if let specificSelf = self as? InputAskForNumber {
                self.id = tempObject.id
                self.inputType = tempObject.inputType.rawValue
                self.title = tempObject.title
                let order = Int32(tempObject.order)
                self.order = order
                self.userActionRequired = tempObject.userActionRequired
                
                specificSelf.allowDecimals = tempObject.allowDecimals
                specificSelf.allowNegatives = tempObject.allowNegatives
                specificSelf.currency = tempObject.currency
                specificSelf.promptBool = tempObject.promptBool
                specificSelf.promptString = tempObject.promptString
                specificSelf.useRange = tempObject.useRange
                specificSelf.defaultValue = tempObject.defaultNumberValue
                specificSelf.maxValue = tempObject.maxNumberValue
                specificSelf.minValue = tempObject.minNumberValue
                specificSelf.stepCount = tempObject.stepCount
            }
        case .calculate:
            if let specificSelf = self as? InputCalculate {
                
            }
        case .currentDatetime:
            if let specificSelf = self as? InputCurrentDatetime {
                
            }
        case .getLocation:
            if let specificSelf = self as? InputGetLocation {
                
            }
        case .setNumber:
            if let specificSelf = self as? InputSetNumber {
                
            }
        case .setText:
            if let specificSelf = self as? InputSetText {
                
            }
        
//        default:
//            break
        }
    }
}

